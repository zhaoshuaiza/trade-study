#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""批量翻页抓取（不用截图）：连绵 ArrowRight -> 章节文本流到达即落盘 -> 长时间无新内容即到末尾。

前置: 受控 Edge 已登录 + 阅读器已切到双栏翻页模式。
用法:
  python _cdp_fetch6.py --book 2015 [--rounds 40] [--batch 40] [--nostart]
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


def title_safe(page):
    try:
        return page.evaluate(
            "() => { const e = document.querySelector('.readerTopBar_title_chapter');"
            " return e ? e.textContent.trim() : ''; }")
    except Exception:
        return "?"


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
    ap.add_argument("--rounds", type=int, default=60)
    ap.add_argument("--batch", type=int, default=40)
    ap.add_argument("--stall", type=int, default=6)
    ap.add_argument("--nostart", action="store_true", help="不跳回开头，从当前位置继续")
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
    stats = {"resp": 0, "chap": 0, "notdec": 0, "short": 0, "dup": 0}

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        ctx = b.contexts[0]
        pages = ctx.pages
        print("pages:", len(pages))
        page = pages[0]
        for pg in pages[1:]:
            try:
                pg.close()
            except Exception:
                pass

        def on_response(resp):
            nonlocal new_count
            stats["resp"] += 1
            last = resp.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in resp.url or not last.startswith("e_"):
                return
            stats["chap"] += 1
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
                print("  [saved] ch%04d %5d字" % (idx, len(text)))

        page.on("response", on_response)

        if not args.nostart:
            page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
            time.sleep(9)
            # 跳回开头：连按左键到顶
            for _ in range(60):
                try:
                    page.keyboard.press("ArrowLeft")
                except Exception:
                    break
                time.sleep(0.12)
            try:
                # 若左键无效则走目录第一项
                t = title_safe(page)
                print("[start] after left keys, title:", t)
            except Exception:
                pass
            time.sleep(2)

        # 焦点落到正文区
        try:
            page.mouse.click(700, 450)
        except Exception:
            pass
        time.sleep(1)

        stall = 0
        for rnd in range(args.rounds):
            before = new_count
            for _ in range(args.batch):
                try:
                    page.keyboard.press("ArrowRight")
                except Exception:
                    pass
                time.sleep(0.22)
            time.sleep(3.0)
            gained = new_count - before
            t = title_safe(page)
            if gained:
                stall = 0
                print("[round %02d] +%d chunks  total=%d  at=%s" % (rnd, gained, new_count, t))
            else:
                stall += 1
                print("[round %02d] no new (stall %d) total=%d  at=%s resp=%d chap=%d dup=%d"
                      % (rnd, stall, new_count, t, stats["resp"], stats["chap"], stats["dup"]))
                if stall >= args.stall:
                    print("[end] reached end of book.")
                    break
            save_meta(out_dir, chapters)

        save_meta(out_dir, chapters)
        print("[done] files:", next_index(out_dir), "| new:", new_count,
              "| chapter-resp:", stats["chap"], "dup:", stats["dup"], "notdec:", stats["notdec"])
        b.close()


if __name__ == "__main__":
    main()
