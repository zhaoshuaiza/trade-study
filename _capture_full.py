#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整慢速双程抓取: 正向翻到书尾 + 反向翻回书首, 覆盖全书(无需章节 hex 锚点)。
匀速慢按(默认 ~3.8s/页), 仅在跨章时产生 1 次正文请求, 远低于限流阈值。

python _capture_full.py --book 2015 [--pause 3.8] [--idle 25]
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
CSS_PREFIX = b"/** "  # 分片首部为 base64("/**"), 解码后前 5 字节


def decode_part(body, hdr=33):
    try:
        s = body[hdr:].decode("latin1")
        return base64.b64decode(s + "=" * ((-len(s)) % 4))
    except Exception:
        return None


def assemble(parts, hdr=33, max_perm=5):
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
    elif n <= max_perm:
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
        if not docs or txt.count("\ufffd"):
            continue
        score = sum(len(d) for d in docs)
        if best is None or score > best[0]:
            best = (score, order, docs)
    return (best[2], [decoded[i][0] for i in best[1]]) if best else ([], None)


def xhtml_to_text(x):
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", x2)
    paras = []
    for b in re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2):
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


def current_chapter(page):
    try:
        t = page.evaluate("() => (document.body.innerText||'')").split("\n")
        return t[4].strip() if len(t) > 4 else "?"
    except Exception:
        return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--pause", type=float, default=3.8)
    ap.add_argument("--idle", type=float, default=25)
    ap.add_argument("--grace", type=float, default=4.5)
    ap.add_argument("--maxpress", type=int, default=2500)
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
    print("[init] 已有去重散列:", len(hashes))

    stats = {"resp": 0, "docs": 0, "dup": 0, "fail": 0}
    new_count = 0
    groups = []
    cur = None

    def add_shard(idx, body):
        nonlocal cur
        now = time.time()
        if idx == 0:
            cur = {"shards": {}, "start": now, "last": now, "sealed": False}
            groups.append(cur)
            cur["shards"][0] = body
        else:
            if cur is not None and (now - cur["start"]) < 1.5 and len(groups) >= 2:
                groups[-2]["shards"][idx] = body
                groups[-2]["last"] = now
            elif cur is not None:
                cur["shards"][idx] = body
                cur["last"] = now
            else:
                cur = {"shards": {}, "start": now, "last": now, "sealed": False}
                groups.append(cur)
                cur["shards"][idx] = body

    def flush_group(g):
        nonlocal new_count
        parts = sorted(g["shards"].items())
        cand = [(i, b) for i, b in parts if decode_part(b) != CSS_PREFIX]
        if len(cand) < 2:
            return []
        docs, _ = assemble(cand)
        if not docs:
            stats["fail"] += 1
            return []
        saved = []
        for d in docs:
            stats["docs"] += 1
            text = xhtml_to_text(d)
            if len(text) < 20:
                continue
            h = hashlib.md5(text.encode("utf-8")).hexdigest()
            if h in hashes:
                stats["dup"] += 1
                continue
            idx = next_index(out_dir)
            html_path = os.path.join(out_dir, "%04d.html" % idx)
            txt_path = os.path.join(out_dir, "%04d.txt" % idx)
            try:
                with open(html_path, "w", encoding="utf-8", newline="") as f:
                    f.write(d); f.flush(); os.fsync(f.fileno())
                with open(txt_path, "w", encoding="utf-8", newline="") as f:
                    f.write(text); f.flush(); os.fsync(f.fileno())
            except Exception as e:
                print("  [write fail] %04d: %s" % (idx, str(e)[:60])); continue
            ok = False
            try:
                with open(txt_path, "rb") as f:
                    rb = f.read().decode("utf-8", "ignore")
                ok = (os.path.getsize(txt_path) > 0 and os.path.getsize(html_path) > 0
                      and hashlib.md5(rb.encode("utf-8")).hexdigest() == h
                      and len(rb) == len(text))
            except Exception as e:
                print("  [verify fail] %04d: %s" % (idx, str(e)[:60]))
            if not ok:
                stats["fail"] += 1
                continue
            hashes.add(h); new_count += 1; saved.append((idx, len(text)))
            print("  [确认落盘] %04d.txt %6d字" % (idx, len(text)))
        return saved

    def settle_ready(now):
        out = []
        for g in list(groups):
            if not g["sealed"] and (now - g["last"]) >= args.grace:
                g["sealed"] = True
                out.extend(flush_group(g))
        return out

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        for pg in ctx.pages[1:]:
            try: pg.close()
            except Exception: pass
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.clearBrowserCache")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

        def on_response(resp):
            url = resp.url
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in url or "e_" not in last:
                return
            try:
                body = resp.body()
            except Exception:
                return
            if not body:
                return
            stats["resp"] += 1
            m = re.search(r"e_e?_(\d+)$", last) or re.search(r"e_(\d+)$", last)
            idx = int(m.group(1)) if m else -1
            if idx >= 0:
                add_shard(idx, body)

        page.on("response", on_response)
        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)
        print("[start] 当前章节《%s》" % current_chapter(page))

        # 预热激活翻页控制器
        for _ in range(3):
            try: page.keyboard.press("ArrowRight")
            except Exception: pass
            time.sleep(args.pause)
        settle_ready(time.time())

        def phase(key, label):
            nonlocal new_count
            print("=== 阶段 %s(%s) ===" % (label, key))
            idle = 0
            for press in range(args.maxpress):
                try:
                    page.keyboard.press(key)
                except Exception:
                    pass
                time.sleep(args.pause)
                now = time.time()
                saved = settle_ready(now)
                disk_n = next_index(out_dir)
                if saved:
                    idle = 0
                    print("[%s 第%04d页] ✓ 落盘%d段 | 《%s》 | 磁盘共%d"
                          % (label, press, len(saved), current_chapter(page), disk_n))
                elif groups and (now - groups[-1]["last"]) < 2:
                    idle = 0
                else:
                    idle += 1
                if idle and idle % 10 == 0:
                    print("   ...%s idle=%d resp=%d docs=%d fail=%d" %
                          (label, idle, stats["resp"], stats["docs"], stats["fail"]))
                if idle >= args.idle:
                    print("[%s] 连续%d页无新内容,本阶段结束" % (label, idle))
                    break

        phase("ArrowRight", "正向(书首→书尾)")
        phase("ArrowLeft", "反向(书尾→书首)")

        print("[收尾] 强制结算残留组...")
        now = time.time()
        for g in groups:
            if not g["sealed"]:
                g["sealed"] = True
                flush_group(g)
        print("[done] 本次新增:%d | docs:%d fail:%d dup:%d | 磁盘文件数:%d"
              % (new_count, stats["docs"], stats["fail"], stats["dup"], next_index(out_dir)))
        b.close()


if __name__ == "__main__":
    main()
