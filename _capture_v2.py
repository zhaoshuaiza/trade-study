#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""改进版逐章抓取: 网络分片(e_N base64) + 突发分组(避免末片迟到错位) +
md5 去重 + fsync 回读确认。支持跳到指定章节锚点(target-k)做定点补齐。
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
CSS_START = ("Lyoq",)  # "/**" 的 base64


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
        if not docs:
            continue
        if txt.count("\ufffd"):
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


def current_chapter(page):
    try:
        t = page.evaluate("() => (document.body.innerText||'')").split("\n")
        return t[4].strip() if len(t) > 4 else "?"
    except Exception:
        return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--target-k", default=None, help="先跳到此 k 锚点(章节)再抓,用于定点补齐")
    ap.add_argument("--key", default="ArrowRight", choices=["ArrowRight", "ArrowLeft"])
    ap.add_argument("--maxpress", type=int, default=600)
    ap.add_argument("--idle", type=int, default=20)
    ap.add_argument("--noreload", action="store_true")
    ap.add_argument("--pause", type=float, default=3.2)
    ap.add_argument("--grace", type=float, default=5.0, help="一组分片静默多久后视为成型可组装")
    ap.add_argument("--home", action="store_true")
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

    # 突发分组: groups 列表, 每组 {shards:{idx:body}, start, last}
    groups = []
    cur = None

    def add_shard(idx, body):
        nonlocal cur
        now = time.time()
        if idx == 0:
            cur = {"shards": {}, "start": now, "last": now}
            groups.append(cur)
            cur["shards"][0] = body
        else:
            # 末片迟到容错: 若当前组刚开(<1.5s)且存在前一组,则归到前一组
            if cur is not None and (now - cur["start"]) < 1.5 and len(groups) >= 2:
                groups[-2]["shards"][idx] = body
                groups[-2]["last"] = now
            elif cur is not None:
                cur["shards"][idx] = body
                cur["last"] = now
            else:
                # 没有 e_0 先到,开一个临时组
                cur = {"shards": {}, "start": now, "last": now}
                groups.append(cur)
                cur["shards"][idx] = body

    def flush_group(g):
        nonlocal new_count
        parts = sorted(g["shards"].items())
        cand = [(i, b) for i, b in parts
                if not (decode_part(b) and decode_part(b)[:5] == b"/** ")]
        if len(cand) < 2:
            return []
        docs, order = assemble(cand)
        if not docs:
            stats["fail"] += 1
            print("  [组 fail] 分片 %s 无法组装(valid doc=0)" % sorted(g["shards"].keys()))
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
                print("  [verify BAD] %04d" % idx); continue
            hashes.add(h); new_count += 1; saved.append((idx, len(text)))
            print("  [确认落盘] %04d.txt %6d字 | 分片%s" % (idx, len(text), sorted(g["shards"].keys())))
        return saved

    def settle_ready(now):
        out = []
        # 成型条件: 距该组最后一片超过 grace 秒
        for g in list(groups):
            if (now - g["last"]) >= args.grace and g.get("sealed") is not True:
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
            if "/web/book/chapter/" not in url or not last.startswith("e_"):
                return
            try:
                body = resp.body()
            except Exception:
                return
            if not body:
                return
            stats["resp"] += 1
            try:
                idx = int(last.split("_")[1])
            except Exception:
                return
            add_shard(idx, body)

        page.on("response", on_response)

        if args.target_k:
            target = "%s?k=%s" % (cfg["reader"], args.target_k)
            print("[target] 跳到章节锚点:", args.target_k)
        else:
            target = cfg["reader"]
        if not args.noreload:
            page.goto(target, wait_until="domcontentloaded", timeout=60000)
            time.sleep(8)
            print("[reload] ok -> 现读《%s》" % current_chapter(page))
        else:
            print("[noreload] 沿用当前页面(已是目标定位)")

        # 预热激活翻页控制器
        print("[activate] 预热(ArrowRight x3)...")
        for _ in range(3):
            try: page.keyboard.press("ArrowRight")
            except Exception: pass
            time.sleep(args.pause)
        settle_ready(time.time())

        idle = 0
        for press in range(args.maxpress):
            before = new_count
            try:
                page.keyboard.press(args.key)
            except Exception:
                pass
            time.sleep(args.pause)
            now = time.time()
            saved = settle_ready(now)
            chap = current_chapter(page)
            disk_n = next_index(out_dir)
            if saved:
                idle = 0
                print("[第%04d页] ✓ 落盘 %d 段 | 《%s》 | 磁盘共%d"
                      % (press, len(saved), chap, disk_n))
            elif stats["resp"] > 0 and (now - groups[-1]["last"] if groups else 0) < 2:
                idle = 0  # 刚有分片,仍在前进
            else:
                idle += 1
            if idle and idle % 10 == 0:
                print("   ...idle=%d 已抓resp=%d docs=%d fail=%d" % (idle, stats["resp"], stats["docs"], stats["fail"]))
            if idle >= args.idle:
                print("[end] 连续 %d 页无新内容,停止" % idle); break

        # 收尾: 强制结算所有未封口组(放宽 grace)
        print("[收尾] 强制结算残留组...")
        for g in groups:
            if not g.get("sealed"):
                g["sealed"] = True
                flush_group(g)
        print("[done] 本次新增:%d | docs:%d fail:%d dup:%d | 磁盘文件数:%d"
              % (new_count, stats["docs"], stats["fail"], stats["dup"], next_index(out_dir)))
        b.close()


if __name__ == "__main__":
    main()
