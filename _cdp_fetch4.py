#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""主抓取脚本：打开目录面板 → 逐项点击 → 捕获 /web/book/chapter/e_N 响应 → 落盘。

用法:
  python _cdp_fetch4.py --book 2015 [--rounds N] [--wait SEC]
"""
import os, re, time, json, base64, hashlib, argparse

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


def decode_body(body):
    if not body or len(body) <= 33:
        return None
    if body[32:33] != b"P":
        return None
    try:
        return base64.b64decode(body[33:]).decode("utf-8", "ignore")
    except Exception:
        return None


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


def ensure_catalog_open(page):
    """确保目录面板可见；返回 True 表示目录项可点击。"""
    if page.locator(".readerCatalog_list_item").count() == 0:
        return False
    # 先把元素挪进视野判断可见性：目录项可能在面板外
    def _visible():
        try:
            box = page.locator(".readerCatalog_list_item").first.bounding_box()
            return bool(box and box["width"] > 0 and box["x"] >= -2)
        except Exception:
            return False

    for sel in ['button.readerControls_item.catalog', '.readerControls_item.catalog',
                '.readerTopBar_link_catalog', 'text=目录', '[class*=catalog][class*=btn]',
                '.readerCatalog_switch', 'button:has-text("目录")']:
        try:
            loc = page.locator(sel).first
            if loc.count():
                loc.click(timeout=4000)
                time.sleep(1.8)
                if _visible():
                    print("[catalog] opened via", sel)
                    return True
                print("[catalog] clicked %s but still hidden" % sel)
        except Exception as e:
            print("[catalog] %s failed: %s" % (sel, str(e)[:60]))
    return _visible()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--wait", type=float, default=2.4)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=0)
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
    state = {"title": ""}

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        ctx = b.contexts[0]
        page = ctx.new_page()

        def on_response(resp):
            nonlocal new_count
            stats["resp"] += 1
            last = resp.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in resp.url or not last.startswith("e_"):
                return
            try:
                body = resp.body()
            except Exception:
                return
            dec = decode_body(body)
            if not dec:
                stats["notdec"] += 1
                return
            for part in re.split(r"</html>", dec):
                part = part.strip()
                if not part or "<" not in part:
                    continue
                xhtml = part if part.endswith("</html>") else part + "</html>"
                _t, text = xhtml_to_text(xhtml)
                if not text or len(text) < 30:
                    stats["short"] += 1
                    continue
                h = hashlib.md5(text.encode("utf-8")).hexdigest()
                if h in hashes:
                    stats["dup"] += 1
                    continue
                hashes.add(h)
                idx = next_index(out_dir)
                with open(os.path.join(out_dir, "%04d.html" % idx), "w", encoding="utf-8") as f:
                    f.write(xhtml)
                with open(os.path.join(out_dir, "%04d.txt" % idx), "w", encoding="utf-8") as f:
                    f.write(text)
                chapters.append({"n": idx, "title": state["title"], "chars": len(text)})
                new_count += 1
                print("  [saved] ch%04d %5d字  |%s" % (idx, len(text), state["title"]))

        page.on("response", on_response)
        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(7)

        ok = ensure_catalog_open(page)
        print("[catalog] visible:", ok)
        total = page.locator(".readerCatalog_list_item").count()
        print("[catalog] items:", total)
        titles = page.evaluate("""() => Array.from(document.querySelectorAll('.readerCatalog_list_item'))
              .map(e => { const t = e.querySelector('[class*=title_text],[class*=title]');
                          return t ? t.textContent.trim() : ''; })""")
        if titles:
            json.dump(titles, open(os.path.join(out_dir, "_toc.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print("[toc] saved", len(titles), "titles")

        if total == 0:
            print("[fatal] no catalog items")
            b.close()
            return

        end = args.end if args.end else total
        for i in range(args.start, end):
            title = titles[i] if i < len(titles) else ""
            state["title"] = title
            before = new_count
            clicked_ok = False
            # 每次先看目录是否还在，不在就用 JS 触发还原的三横线按钮
            page.evaluate("""() => {
                const list = document.querySelector('.readerCatalog_list_item');
                if (!list) {
                    const b = document.querySelector('button.readerControls_item.catalog');
                    if (b) b.click();
                }
            }""")
            time.sleep(0.8)
            try:
                page.locator(".readerCatalog_list_item").nth(i).click(timeout=3500)
                clicked_ok = True
            except Exception:
                pass
            if not clicked_ok:
                # 兜底：JS 点击
                try:
                    page.evaluate("""(idx) => {
                        const items = document.querySelectorAll('.readerCatalog_list_item');
                        if (items[idx]) items[idx].click();
                    }""", i)
                except Exception:
                    pass
            # 等到本轮没有新内容为止
            for _ in range(int(args.wait / 0.5) or 1):
                time.sleep(0.5)
                if new_count > before:
                    time.sleep(0.8)
            print("[%3d/%3d] %-26s new=%d total=%d" % (i, total, title[:22], new_count - before, new_count))

        try:
            old = json.load(open(os.path.join(out_dir, "_meta.json"), encoding="utf-8"))
        except Exception:
            old = []
        merged = {c["n"]: c for c in (old + chapters)}
        json.dump([merged[k] for k in sorted(merged)],
                  open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("[done] files:", next_index(out_dir), "| new this run:", new_count)
        b.close()


if __name__ == "__main__":
    main()
