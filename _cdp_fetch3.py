#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""滚动式逐章抓取：先把阅读位置拉回开头，再持续下滚，触发分章内容加载。

用法:
  python _cdp_fetch3.py --book 2015 [--rounds N] [--max N] [--restart]
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


def cur_title(page):
    try:
        return page.evaluate("""() => { const e = document.querySelector('.readerTopBar_title_chapter');
                                        return e ? e.textContent.trim() : ''; }""")
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--rounds", type=int, default=300)
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--step", type=int, default=1800)
    ap.add_argument("--wait", type=float, default=1.6)
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
    print("[init] existing:", len(hashes), "next idx:", next_index(out_dir))

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
            last = resp.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in resp.url or not last.startswith("e_"):
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
                chapters.append({"n": idx, "title": state["title"], "chars": len(text)})
                new_count += 1
                print("  [saved] ch%04d chars=%d  |%s" % (idx, len(text), state["title"]))

        page.on("response", on_response)
        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        # 回到书的最开头
        page.evaluate("() => window.scrollTo(0, 0)")
        time.sleep(2)
        try:
            page.keyboard.press("Home")
        except Exception:
            pass
        time.sleep(2)
        print("[start] title ->", cur_title(page))

        stall = 0
        for rnd in range(args.rounds):
            if args.max and new_count >= args.max:
                print("[done] max reached")
                break
            before = new_count
            t = cur_title(page)
            if t:
                state["title"] = t
            page.mouse.wheel(0, args.step)
            time.sleep(args.wait)
            if new_count == before:
                stall += 1
                if stall % 10 == 0:
                    print("  [stall %d] round %d  current=%s" % (stall, rnd, cur_title(page)))
                if stall >= 40:
                    print("[stop] stalled. new:", new_count)
                    break
            else:
                stall = 0
                print("  [r%03d] total=%d  at=%s" % (rnd, new_count, cur_title(page)))

        try:
            old = json.load(open(os.path.join(out_dir, "_meta.json"), encoding="utf-8"))
        except Exception:
            old = []
        merged = {c["n"]: c for c in (old + chapters)}
        json.dump([merged[k] for k in sorted(merged)],
                  open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("[summary] files:", next_index(out_dir), "| new:", new_count)
        b.close()


if __name__ == "__main__":
    main()
