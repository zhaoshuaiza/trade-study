#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按目录项定点抓取: 点击目录中的每一节 -> 等待内容请求 -> 组装落盘 -> 确认后才进入下一节。

复用 _cdp_fetch_page 的解码/组装/去重/回读校验逻辑。
python _cdp_fetch_catalog.py --book 2015 [--start 0] [--limit 20] [--wait 6]
"""
import os, re, sys, time, json, argparse, hashlib

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import _cdp_fetch_page as old  # noqa: E402

from playwright.sync_api import sync_playwright  # noqa: E402

BOOKS = old.BOOKS
CSS_START = old.CSS_START


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=10, help="处理多少个目录项,0=全部")
    ap.add_argument("--wait", type=float, default=6.0, help="点击后等待秒数")
    ap.add_argument("--ids", default="", help="逗号分隔的目录下标,优先于 start/limit")
    args = ap.parse_args()

    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)

    hashes = set()
    for f in os.listdir(out_dir):
        if re.match(r"\d+\.txt$", f):
            try:
                hashes.add(hashlib.md5(open(os.path.join(out_dir, f), encoding="utf-8").read()
                                       .encode("utf-8")).hexdigest())
            except Exception:
                pass
    print("[init] 已有片段 %d" % len(hashes))

    cur = []
    ready = []
    stats = {"resp": 0, "docs": 0, "dup": 0, "fail": 0}

    def flush_group(group):
        saved = []
        parts = sorted(group, key=lambda x: x[1])
        cand = [(i, b) for _, i, b in parts
                if not any(b[33:].decode("latin1", "ignore").startswith(p) for p in CSS_START)]
        if not cand:
            return saved
        docs, order = old.assemble(cand)
        if not docs:
            stats["fail"] += 1
            return saved
        for d in docs:
            stats["docs"] += 1
            text = old.xhtml_to_text(d)
            if len(text) < 20:
                continue
            h = hashlib.md5(text.encode("utf-8")).hexdigest()
            if h in hashes:
                stats["dup"] += 1
                continue
            idx = old.next_index(out_dir)
            hp = os.path.join(out_dir, "%04d.html" % idx)
            tp = os.path.join(out_dir, "%04d.txt" % idx)
            try:
                with open(hp, "w", encoding="utf-8", newline="") as f:
                    f.write(d); f.flush(); os.fsync(f.fileno())
                with open(tp, "w", encoding="utf-8", newline="") as f:
                    f.write(text); f.flush(); os.fsync(f.fileno())
            except Exception as e:
                print("  [write fail] %s" % str(e)[:60]); continue
            ok = False
            try:
                rb = open(tp, "rb").read().decode("utf-8", "ignore")
                ok = (os.path.getsize(tp) > 0 and os.path.getsize(hp) > 0
                      and hashlib.md5(rb.encode("utf-8")).hexdigest() == h
                      and len(rb) == len(text))
            except Exception as e:
                print("  [verify fail] %s" % str(e)[:60])
            if not ok:
                stats["fail"] += 1
                print("  [verify BAD] %04d" % idx); continue
            hashes.add(h)
            saved.append((idx, len(text)))
            print("  [已确认落盘] %04d.txt %6d字" % (idx, len(text)))
        return saved

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try:
                pg.close()
            except Exception:
                pass
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.enable")
            cdp.send("Network.clearBrowserCache")
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            print("[cdp] 已清浏览器缓存")
        except Exception as e:
            print("[cdp] fail", str(e)[:60])

        def on_response(resp):
            last = resp.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in resp.url or not last.startswith("e_"):
                return
            try:
                idx = int(last.split("_")[1])
                body = resp.body()
            except Exception:
                return
            stats["resp"] += 1
            if idx == 0:
                if cur:
                    ready.append(list(cur))
                cur[:] = [(time.time(), idx, body)]
            else:
                cur.append((time.time(), idx, body))

        page.on("response", on_response)

        try:
            page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(8)

        nitems = page.evaluate(
            "() => document.querySelectorAll('.readerCatalog_list_item').length")
        titles = page.evaluate(
            "() => Array.from(document.querySelectorAll('.readerCatalog_list_item')).map(e=>e.innerText.trim())")
        print("[toc] 目录项 %d" % nitems)
        json.dump(titles, open(os.path.join(out_dir, "_toc.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

        if args.ids:
            idlist = [int(x) for x in args.ids.split(",") if x.strip() != ""]
        else:
            end = nitems if args.limit == 0 else min(nitems, args.start + args.limit)
            idlist = list(range(args.start, end))

        click_js = """(i) => {
          const el = document.querySelectorAll('.readerCatalog_list_item')[i];
          if (!el) return 'no-el';
          const t = el.querySelector('.readerCatalog_list_item_title') || el;
          t.scrollIntoView({block:'center'});
          t.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));
          t.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));
          t.dispatchEvent(new MouseEvent('click',{bubbles:true}));
          return 'ok';
        }"""

        got_new = 0
        for step, i in enumerate(idlist, 1):
            try:
                r = page.evaluate(click_js, i)
            except Exception as e:
                print("[%d] 目录项%d 点击异常 %s" % (step, i, str(e)[:50]))
                continue
            before = cur + [x for g in ready for x in g]
            deadline = time.time() + args.wait
            while time.time() < deadline:
                time.sleep(0.5)
            now = cur + [x for g in ready for x in g]
            ncur_before = len(ready) + (1 if cur else 0)
            # 先把已封口的组落盘
            newly = 0
            if cur:
                ready.append(list(cur))
                cur[:] = []
            while ready:
                g = ready.pop(0)
                sv = flush_group(g)
                newly += len(sv)
            got_new += newly
            url = page.url
            chap = old.current_chapter(page)
            print("[%d/%d] 目录项%d《%s》 -> 新请求%d 新落盘%d | 现读《%s》 | %s"
                  % (step, len(idlist), i, (titles[i] if i < len(titles) else "?")[:22],
                     len(now) - len(before), newly, chap, url[-28:]))
            if newly == 0:
                cov = old.toc_coverage(out_dir)
                if cov:
                    print("     目录覆盖 %d/%d" % cov)

        print("[done] 本次新落盘 %d | stats %s" % (got_new, stats))
        cov = old.toc_coverage(out_dir)
        if cov:
            print("[done] 目录覆盖 %d/%d" % cov)


if __name__ == "__main__":
    main()
