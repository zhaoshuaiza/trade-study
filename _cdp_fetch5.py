#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""双栏翻页模式抓取：回到书首 -> 连续按 ArrowRight 翻页 -> 捕获章节内容流落盘。

前置：受控 Edge 已登录、阅读器已切换为双栏(翻页)模式。
用法:
  python _cdp_fetch5.py --book 2015 [--iters 4000] [--gaps 60]
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
    ap.add_argument("--iters", type=int, default=5000)
    ap.add_argument("--gaps", type=int, default=80, help="连续多少轮无变化则认定到书末")
    ap.add_argument("--fast", type=float, default=0.75)
    ap.add_argument("--slow", type=float, default=1.6)
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
    stats = {"resp": 0, "notdec": 0, "short": 0, "dup": 0}

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
                print("  [saved] ch%04d %5d字 |%s" % (idx, len(text), state["title"]))

        page.on("response", on_response)
        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)

        # ---- 回到书首：打开目录点第一项 ----
        try:
            page.locator("button.readerControls_item.catalog").first.click(timeout=6000)
            time.sleep(2)
            page.evaluate("""() => {
                const it = document.querySelectorAll('.readerCatalog_list_item')[0];
                if (it) it.click();
            }""")
            time.sleep(3)
            print("[jump] back to first item, title ->", cur_title(page))
        except Exception as e:
            print("[jump] catalog failed:", str(e)[:90])

        # ---- 开始翻页 ----
        last_title = cur_title(page)
        gap = 0
        for it in range(args.iters):
            t = cur_title(page)
            if t and t != state["title"]:
                if state["title"]:
                    print("[ch] %s" % t)
                state["title"] = t
            before = new_count
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(args.slow if new_count > before else args.fast)
            # 翻页后给新章节一点加载时间
            if new_count > before:
                time.sleep(1.0)
                gap = 0
            else:
                t2 = cur_title(page)
                if t2 == last_title:
                    gap += 1
                else:
                    gap = 0
                last_title = t2
                if gap and gap % 20 == 0:
                    print("[idle %d] iter=%d at=%s saved=%d resp=%d dup=%d"
                          % (gap, it, t2, new_count, stats["resp"], stats["dup"]))
                if gap >= args.gaps:
                    print("[end] no progress for %d rounds. done." % args.gaps)
                    break
            if it % 50 == 0:
                print("[iter %d] saved=%d at=%s" % (it, new_count, cur_title(page)))
                save_meta(out_dir, chapters)

        save_meta(out_dir, chapters)
        print("[done] files:", next_index(out_dir), "| new:", new_count,
              "| resp:", stats["resp"], "dup:", stats["dup"], "notdec:", stats["notdec"])
        b.close()


if __name__ == "__main__":
    main()
