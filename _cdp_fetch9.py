#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""自适应节奏翻页抓取: 按一下 -> 等内容请求跟上 -> 再按。

关键改进: 之前固定 0.22s 一按,导致内容请求被取消;
现在每次按键后等待 until 距上次响应 >0.45s 或超时 2.5s,保证加载完成。
"""
import os, re, time, json, base64, hashlib, itertools, argparse

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
CSS_START = ("Lyoq",)


def decode_part(body, hdr=33):
    try:
        s = body[hdr:].decode("latin1")
        return base64.b64decode(s + "=" * ((-len(s)) % 4))
    except Exception:
        return None


def assemble(parts, hdr=33):
    decoded = []
    for i, b in parts:
        raw = decode_part(b, hdr)
        if raw:
            decoded.append((i, raw))
    if not decoded:
        return [], None
    n = len(decoded)
    orders = [(0,)] if n == 1 else (list(itertools.permutations(range(n))) if n <= 5 else [tuple(range(n))])
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
        if bad:
            continue
        score = sum(len(d) for d in docs)
        if best is None or score > best[0]:
            best = (score, order, docs)
    return (best[2], [decoded[i][0] for i in best[1]]) if best else ([], None)


def xhtml_to_text(x):
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", "", x2)
    blocks = re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras = []
    for b in blocks:
        t = re.sub(r"<[^>]+>", "", b).replace("&nbsp;", " ")
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return "\n\n".join(paras)


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
    ap.add_argument("--maxpress", type=int, default=3000)
    ap.add_argument("--key", default="ArrowRight", choices=["ArrowRight", "ArrowLeft"])
    ap.add_argument("--noreload", action="store_true")
    ap.add_argument("--idle", type=int, default=25, help="连续多少次按键无新章则认定到末尾")
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
    print("[init] existing chunks:", len(hashes))

    chapters = []
    new_count = 0
    pending = []
    last_resp_ts = [time.time()]
    stats = {"resp": 0, "docs": 0, "dup": 0, "fail": 0}

    def flush(group):
        nonlocal new_count
        parts = sorted(group, key=lambda x: x[1])
        cand = [(i, b) for _, i, b in parts
                if not any(b[33:].decode("latin1", "ignore").startswith(p) for p in CSS_START)]
        if not cand:
            return
        docs, order = assemble(cand)
        if not docs:
            stats["fail"] += 1
            return
        for d in docs:
            stats["docs"] += 1
            text = xhtml_to_text(d)
            if len(text) < 20:
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
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try:
                pg.close()
            except Exception:
                pass
        try:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            print("[cdp] cache disabled")
        except Exception as e:
            print("[cdp] fail", str(e)[:80])

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
            last_resp_ts[0] = time.time()

        page.on("response", on_response)

        # 先重载阅读器,确保后续请求真实发生
        if args.noreload:
            print("[reload] skipped")
        else:
            try:
                page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
                time.sleep(9)
                print("[reload] ok")
            except Exception as e:
                print("[reload] fail", str(e)[:80])

        # 回到扉页: 目录跳首 + 左键到底
        for attempt in range(2):
            try:
                page.locator("button.readerControls_item.catalog").first.click(timeout=5000)
            except Exception:
                page.evaluate("""() => {const b=document.querySelector('button.readerControls_item.catalog'); if(b) b.click();}""")
            time.sleep(1.8)
            page.evaluate("""() => {const it=document.querySelectorAll('.readerCatalog_list_item')[0]; if(it) it.click();}""")
            time.sleep(3)
            try:
                page.mouse.click(700, 450)
            except Exception:
                pass
            time.sleep(1)
        for _ in range(40):
            try:
                page.keyboard.press("ArrowLeft")
            except Exception:
                break
            time.sleep(0.5)
        # 结算首页带出来的内容
        while pending:
            g, seen = [], set()
            while pending:
                t, i, bd = pending.pop(0)
                if i in seen:
                    pending.insert(0, (t, i, bd))
                    break
                seen.add(i)
                g.append((t, i, bd))
            if g:
                flush(g)
        print("[start] 回到扉页完成, 已有 %d 段" % new_count)

        idle = 0
        for press in range(args.maxpress):
            before = new_count
            try:
                page.keyboard.press(args.key)
            except Exception:
                pass
            # 等待本页内容跟上: 直到超过 0.5s 没有新响应, 最多等 2.6s
            t0 = time.time()
            while time.time() - last_resp_ts[0] < 0.5 and time.time() - t0 < 2.6:
                time.sleep(0.1)
            # 结算
            while pending:
                g, seen = [], set()
                while pending:
                    t, i, bd = pending.pop(0)
                    if i in seen:
                        pending.insert(0, (t, i, bd))
                        break
                    seen.add(i)
                    g.append((t, i, bd))
                if g:
                    flush(g)

            if new_count > before:
                idle = 0
                print("[%04d] +%d total=%d" % (press, new_count - before, new_count))
            else:
                idle += 1
                if idle % 10 == 0:
                    print("[%04d] idle %d total=%d resp=%d fail=%d" % (press, idle, new_count, stats["resp"], stats["fail"]))
                if idle >= args.idle:
                    print("[end] 停止, idle=%d" % idle)
                    break
            if press % 100 == 0 and press:
                save_meta(out_dir, chapters)

        save_meta(out_dir, chapters)
        print("[done] files:", next_index(out_dir), "| new:", new_count, "| stats:", stats)
        b.close()


if __name__ == "__main__":
    main()
