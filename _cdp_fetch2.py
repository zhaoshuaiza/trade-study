#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 CDP 连接受控 Edge（已扫码登录），逐章抓取微信读书 content 并落盘。

用法:
  python _cdp_fetch2.py --book 2015 [--max N] [--wait SEC]

核心:
  - 翻章按钮真实选择器: button.readerFooter_button:has-text("下一章")
  - 内容接口: /web/book/chapter/e_N -> base64 分块 -> XHTML
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


def get_toc(page):
    """从目录面板抓取全部章节标题（DOM 中的 readerCatalog_list_item_title_text）。"""
    try:
        return page.evaluate("""() => {
            const els = document.querySelectorAll('.readerCatalog_list_item_title_text, .readerCatalog_list_item_title');
            return Array.from(els).map(e => (e.textContent||'').trim()).filter(Boolean);
        }""")
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--wait", type=float, default=2.2)
    ap.add_argument("--rounds", type=int, default=400)
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
    print("[init] existing chunks:", len(hashes), "-> next index:", next_index(out_dir))

    chapters = []
    new_count = 0

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        ctx = b.contexts[0]
        cs = ctx.cookies()
        wr = {c["name"] for c in cs if "weread" in (c.get("domain") or "")}
        print("weread cookies:", len(wr), "| wr_skey:", "YES" if "wr_skey" in wr else "NO")

        page = ctx.new_page()
        state = {"cur_title": ""}

        def on_response(resp):
            nonlocal new_count
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in url or not last.startswith("e_"):
                return
            try:
                body = resp.body()
            except Exception:
                return
            dec = decode_body(body)
            if not dec:
                return
            for part in re.split(r"</html>", dec):
                part = part.strip()
                if not part or "<" not in part:
                    continue
                xhtml = part if part.endswith("</html>") else part + "</html>"
                _t, text = xhtml_to_text(xhtml)
                if not text or len(text) < 40:
                    continue
                h = hashlib.md5(text.encode("utf-8")).hexdigest()
                if h in hashes:
                    continue
                hashes.add(h)
                idx = next_index(out_dir)
                with open(os.path.join(out_dir, "%04d.html" % idx), "w", encoding="utf-8") as f:
                    f.write(xhtml)
                with open(os.path.join(out_dir, "%04d.txt" % idx), "w", encoding="utf-8") as f:
                    f.write(text)
                chapters.append({"n": idx, "title": state["cur_title"], "chars": len(text)})
                new_count += 1
                print("  [saved] ch%04d chars=%d title=%r" % (idx, len(text), state["cur_title"]))

        page.on("response", on_response)
        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        toc = get_toc(page)
        if toc:
            print("[toc] chapters in catalog:", len(toc))
            with open(os.path.join(out_dir, "_toc.json"), "w", encoding="utf-8") as f:
                json.dump(toc, f, ensure_ascii=False, indent=1)

        stall = 0
        for rnd in range(args.rounds):
            if args.max and new_count >= args.max:
                print("[done] reached --max", args.max)
                break
            before = new_count
            try:
                state["cur_title"] = page.evaluate(
                    "() => { const e = document.querySelector('.readerTopBar_title_chapter'); return e ? e.textContent.trim() : ''; }")
            except Exception:
                pass
            clicked = False
            try:
                btn = page.locator('button.readerFooter_button:has-text("下一章")')
                if btn.count():
                    btn.first.click(timeout=8000)
                    clicked = True
            except Exception:
                pass
            if not clicked:
                try:
                    page.keyboard.press("End")
                    page.mouse.wheel(0, 3000)
                except Exception:
                    pass
            time.sleep(args.wait)
            if new_count == before:
                stall += 1
                if stall % 5 == 0:
                    print("  [stall] round %d no new content (%d consecutive)" % (rnd, stall))
                if stall >= 25:
                    print("[stop] no progress for 25 rounds. new:", new_count)
                    break
            else:
                stall = 0
                print("  [round %d] total new: %d" % (rnd, new_count))

        try:
            old = json.load(open(os.path.join(out_dir, "_meta.json"), encoding="utf-8"))
        except Exception:
            old = []
        merged = {c["n"]: c for c in (old + chapters)}
        json.dump([merged[k] for k in sorted(merged)],
                  open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("[summary] files:", next_index(out_dir), "| new this run:", new_count)
        b.close()


if __name__ == "__main__":
    main()
