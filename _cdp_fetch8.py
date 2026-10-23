#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终版: 双栏翻页 + 分片重组解码。

要点:
  1. 同一批次响应按超时分组 -> 一组 = 一个资源
  2. 剔除样式表分片(payload 以 'Lyoq' 起始)
  3. 剩余分片尝试排列组合 -> 选出能还原出完整 <?xml...</html> 的顺序
  4. 按 </html> 切分 -> 去重 -> 落盘
用法: python _cdp_fetch7.py --book 2015 [--rounds N] [--batch M]
"""
import os, re, sys, time, json, base64, hashlib, itertools, argparse

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS = {
    "2015": {
        "reader": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
        "out": os.path.join(ROOT, "raw/distilled/steenbarger-2015-zh"),
    },
    "2002": {
        "reader": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
        "out": os.path.join(ROOT, "raw/distilled/steenbarger-2002-zh"),
    },
}

CSS_START = ("Lyoq",)   # '/*' 的 base64 前缀,用于识别样式表分片


def loose_b64(s):
    try:
        pad = (-len(s)) % 4
        return base64.b64decode(s + "=" * pad)
    except Exception:
        return None


def decode_part(body, hdr=33):
    """单分片独立 base64 解码 (33 字节头之后)。"""
    try:
        s = body[hdr:].decode("latin1")
        return base64.b64decode(s + "=" * ((-len(s)) % 4))
    except Exception:
        return None


def assemble(parts, hdr=33):
    """把分片的解码字节按正确顺序拼接,选出能还原完整 XHTML 的方案。

    实测: 微信读书把同一段字节流拆成 e_0/e_1/e_3 三片分别独立 base64 编码,
    正确拼接顺序为 0 -> 3 -> 1 (e_2 是样式表,需剔除)。
    """
    decoded = []
    for i, b in parts:
        raw = decode_part(b, hdr)
        if raw:
            decoded.append((i, raw))
    if not decoded:
        return [], None
    n = len(decoded)
    if n == 1:
        orders = [(0,)]
    elif n <= 5:
        orders = list(itertools.permutations(range(n)))
    else:
        orders = [tuple(range(n))]
    best = None
    for order in orders:
        joined = b"".join(decoded[i][1] for i in order)
        if len(joined) < 40:
            continue
        txt = joined.decode("utf-8", "ignore")
        docs = re.findall(r"<\?xml[\s\S]*?</html>", txt)
        if not docs:
            continue
        bad = txt.count("\ufffd")
        score = sum(len(d) for d in docs) - bad * 500
        if bad == 0 and (best is None or score > best[0]):
            best = (score, order, docs)
    if best:
        return best[2], [decoded[i][0] for i in best[1]]
    return [], None


def xhtml_to_text(x):
    m = re.search(r"<title>(.*?)</title>", x, re.S)
    title = m.group(1).strip() if m else ""
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", "", x2)
    blocks = re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras = []
    for b in blocks:
        t = re.sub(r"<[^>]+>", "", b).replace("&nbsp;", " ")
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return title, "\n\n".join(paras)


def next_index(out_dir):
    n = 0
    for f in os.listdir(out_dir) if os.path.isdir(out_dir) else []:
        m = re.match(r"(\d+)\.txt$", f)
        if m:
            n = max(n, int(m.group(1)) + 1)
    return n


def save_meta(out_dir, chapters):
    try:
        old = json.load(open(os.path.join(out_dir, "_meta.json"), encoding="utf-8"))
    except Exception:
        old = []
    merged = {c["n"]: c for c in (old + chapters)}
    json.dump([merged[k] for k in sorted(merged)],
              open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--rounds", type=int, default=120)
    ap.add_argument("--batch", type=int, default=40)
    ap.add_argument("--stall", type=int, default=8)
    ap.add_argument("--nostart", action="store_true")
    args = ap.parse_args()

    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)

    hashes = set()
    for f in os.listdir(out_dir):
        if re.match(r"\d+\.txt$", f):
            try:
                with open(os.path.join(out_dir, f), encoding="utf-8") as fh:
                    hashes.add(hashlib.md5(fh.read().encode("utf-8")).hexdigest())
            except Exception:
                pass
    print("[init] existing chunks:", len(hashes), "next idx:", next_index(out_dir))

    chapters = []
    new_count = 0
    pending = []          # [(t, idx, body)]
    stats = {"resp": 0, "groups": 0, "docs": 0, "dup": 0, "short": 0, "fail": 0}

    def flush(group):
        nonlocal new_count
        parts = sorted(group, key=lambda x: x[1])
        # 剔除样式表分片
        cand = [(i, b) for _, i, b in parts
                if not any(b[33:].decode("latin1", "ignore").startswith(p) for p in CSS_START)]
        if not cand:
            return
        stats["groups"] += 1
        docs, order = assemble(cand)
        if not docs:
            stats["fail"] += 1
            return
        for d in docs:
            stats["docs"] += 1
            _t, text = xhtml_to_text(d)
            if len(text) < 20:
                stats["short"] += 1
                continue
            h = hashlib.md5(text.encode("utf-8")).hexdigest()
            if h in hashes:
                stats["dup"] += 1
                continue
            hashes.add(h)
            idx = next_index(out_dir)
            with open(os.path.join(out_dir, "%04d.html" % idx), "w", encoding="utf-8") as f:
                f.write(d)
            with open(os.path.join(out_dir, "%04d.txt" % idx), "w", encoding="utf-8") as f:
                f.write(text)
            chapters.append({"n": idx, "chars": len(text)})
            new_count += 1
            print("  [saved] ch%04d %6d字" % (idx, len(text)))

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        ctx = b.contexts[0]
        pages = ctx.pages
        page = pages[0]
        for pg in pages[1:]:
            try:
                pg.close()
            except Exception:
                pass

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
            pending.append((time.time(), idx, body))

        # 关键: 关闭缓存,否则二次翻页不再产生网络响应
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            print("[cdp] cache disabled")
        except Exception as e:
            print("[cdp] disable cache failed:", str(e)[:90])

        def jump_to_start(pg):
            """用目录跳回首章(比方向键可靠,尤其已翻到书末时)。"""
            for attempt in range(3):
                try:
                    pg.locator("button.readerControls_item.catalog").first.click(timeout=5000)
                except Exception:
                    try:
                        pg.evaluate("""() => { const b=document.querySelector('button.readerControls_item.catalog');
                                              if (b) b.click(); }""")
                    except Exception:
                        pass
                time.sleep(1.8)
                try:
                    pg.evaluate("""() => { const it=document.querySelectorAll('.readerCatalog_list_item')[0];
                                          if (it) it.click(); }""")
                except Exception:
                    pass
                time.sleep(3.0)
                try:
                    pg.mouse.click(700, 450)
                except Exception:
                    pass
                time.sleep(1.0)
                try:
                    txt = pg.evaluate("() => (document.body.innerText||'')")
                    at_end = ("全书完" in txt)
                except Exception:
                    at_end = True
                print("[jump] attempt %d, at_end=%s" % (attempt, at_end))
                if not at_end:
                    return True
            return False

        page.on("response", on_response)

        if not args.nostart:
            page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
            time.sleep(9)
            jump_to_start(page)
            # 目录跳转后再补几下左键,确保贴到首页
            for _ in range(20):
                try:
                    page.keyboard.press("ArrowLeft")
                except Exception:
                    break
                time.sleep(0.12)
            time.sleep(3)
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass

        ensure_catalog = """() => {
            const list = document.querySelectorAll('.readerCatalog_list_item');
            if (!list.length) {
                const b = document.querySelector('button.readerControls_item.catalog');
                if (b) b.click();
                return false;
            }
            return true;
        }"""
        total_items = 0
        try:
            total_items = page.evaluate("() => document.querySelectorAll('.readerCatalog_list_item').length")
        except Exception:
            pass
        print("[nav] catalog items:", total_items)

        def settle():
            while pending:
                group, seen = [], set()
                while pending:
                    t, i, bd = pending.pop(0)
                    if i in seen:
                        pending.insert(0, (t, i, bd))
                        break
                    seen.add(i)
                    group.append((t, i, bd))
                if group:
                    flush(group)

        for i in range(total_items):
            try:
                page.evaluate(ensure_catalog)
                time.sleep(0.5)
                page.evaluate("""(idx) => {
                    const items = document.querySelectorAll('.readerCatalog_list_item');
                    if (items[idx]) items[idx].click();
                }""", i)
            except Exception:
                pass
            time.sleep(2.2)
            before = new_count
            settle()
            if new_count > before:
                print("[%3d/%d] +%d total=%d" % (i, total_items, new_count - before, new_count))
            if (i + 1) % 10 == 0:
                print("  ...progress %d/%d total_chunks=%d" % (i + 1, total_items, new_count))
                save_meta(out_dir, chapters)

        save_meta(out_dir, chapters)
        print("[done] files:", next_index(out_dir), "| new:", new_count, "| stats:", stats)
        b.close()


if __name__ == "__main__":
    main()
