#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 CDP 连上 headless Edge（真实 profile，完整登录态），逐章抓取并落盘。"""
import os, re, base64, json, argparse

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()

    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)

    saved = set()
    for f in os.listdir(out_dir):
        if re.match(r"\d+\.txt$", f):
            try:
                with open(os.path.join(out_dir, f), encoding="utf-8") as fh:
                    saved.add(hash(fh.read()))
            except Exception:
                pass
    hashes = set(saved)
    chapters = []
    new_count = 0

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("CONNECTED OK")
        ctx = b.contexts[0]

        cs = ctx.cookies()
        wr = {c["name"]: c["value"] for c in cs if "weread" in (c.get("domain") or "")}
        print("weread cookies:", len(wr),
              "| wr_rt:", "YES" if "wr_rt" in wr else "NO",
              "| wr_skey:", "YES" if "wr_skey" in wr else "NO")

        probe = ctx.new_page()
        try:
            r = probe.request.get("https://weread.qq.com/web/shelf/sync",
                                  headers={"Referer": "https://weread.qq.com/"})
            print("shelf/sync:", r.text()[:160])
        except Exception as e:
            print("shelf err:", repr(e))
        probe.close()

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
                title, text = xhtml_to_text(xhtml)
                if not text or len(text) < 50:
                    continue
                h = hash(text)
                if h in hashes:
                    continue
                hashes.add(h)
                idx = next_index(out_dir)
                with open(os.path.join(out_dir, f"{idx:04d}.html"), "w", encoding="utf-8") as f:
                    f.write(xhtml)
                with open(os.path.join(out_dir, f"{idx:04d}.txt"), "w", encoding="utf-8") as f:
                    f.write(text)
                chapters.append({"n": idx, "title": title, "chars": len(text)})
                new_count += 1
                print(f"  [saved] ch{idx:04d} {title!r} chars={len(text)}")

        page = ctx.new_page()
        page.on("response", on_response)
        print("[goto]", cfg["reader"])
        page.goto(cfg["reader"], wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        print("after load -> new:", new_count)

        turn = 0
        while True:
            if args.max and new_count >= args.max:
                print("[done] reached --max:", args.max)
                break
            before = new_count
            try:
                page.mouse.click(700, 450)
            except Exception:
                pass
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(900)
            try:
                btn = page.query_selector("text=下一章")
                if btn:
                    btn.click()
            except Exception:
                pass
            page.wait_for_timeout(1800)
            if new_count == before:
                turn += 1
                if turn >= 3:
                    print("[stop] no new chapters. total new:", new_count)
                    break
            else:
                turn = 0

        try:
            old = json.load(open(os.path.join(out_dir, "_meta.json"), encoding="utf-8"))
        except Exception:
            old = []
        merged = {c["n"]: c for c in (old + chapters)}
        json.dump([merged[k] for k in sorted(merged)],
                  open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("[summary] total files:", next_index(out_dir), "| new:", new_count)
        page.close()


main()
