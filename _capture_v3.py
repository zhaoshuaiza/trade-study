#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整慢速双程抓取 v3: 用 CDP 原生 Network.getResponseBody 读分片 body,
避开 Playwright resp.body() 的 target-swap 竞态(BODYERR)。其余沿用 v2 的组装/去重/落盘。

python _capture_v3.py --book 2015 [--pause 3.8] [--idle 25] [--maxpress 2500]
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
GROUP_GAP = 2.0      # 归属同一章的分片到达间隔上限(秒); 超过则另起一组


def decode_part(body, hdr=33):
    try:
        s = body[hdr:].decode("latin1")
        return base64.b64decode(s + "=" * ((-len(s)) % 4))
    except Exception:
        return None


def is_css(dec):
    """CSS 分片的判定: 解码后以 '/** ' 开头, 或前 200 字节内含典型 css 选择器"""
    return dec[:5] == CSS_PREFIX or b"frontCover" in dec[:200] or b"{r\n" in dec[:200]


def best_join(parts, hdr=33, max_perm=5):
    """把所有分片拼成可读文本, 永不返回 None(除非完全没有可解码分片)。

    优先级: ① 能还原 <?xml...</html> 的排列 > ② 以 <?xml 开头的前缀 > ③ 按 idx 顺序硬拼。
    这样即使某一分片缺失(没有 </html>)也不会丢正文 —— 正文在每个分片里本来就可读。
    """
    dec = []
    for i, b in parts:
        d = decode_part(b, hdr)
        if d and not is_css(d):
            dec.append((i, d))
    if not dec:
        return None, None
    nats = sorted(range(len(dec)), key=lambda k: dec[k][0])
    if len(dec) == 1:
        orders = [(0,)]
    elif len(dec) <= max_perm:
        orders = list(itertools.permutations(range(len(dec))))
    else:
        orders = [tuple(nats)]
    best = None
    for order in orders:
        joined = b"".join(dec[k][1] for k in order)
        if len(joined) < 40:
            continue
        try:
            txt = joined.decode("utf-8")   # 严格解码: 有乱码则该排列无效
        except UnicodeDecodeError:
            continue
        if "\ufffd" in txt:
            continue
        blocks = re.findall(r"<\?xml[\s\S]*?</html>", txt)
        if blocks:
            cand, score = "\n".join(blocks), 10 ** 7 + sum(len(x) for x in blocks)
        elif txt.lstrip().startswith("<?xml"):
            cand, score = txt, 10 ** 6 + len(txt)
        else:
            continue
        if best is None or score > best[0]:
            best = (score, cand, [dec[k][0] for k in order])
    if best is not None:
        return best[1], best[2]
    # 终极兜底: 按 idx 顺序硬拼, 彻底放弃结构校验
    joined = b"".join(dec[k][1] for k in nats)
    txt = joined.decode("utf-8", "ignore")
    if len(txt) < 40:
        return None, None
    return txt, [dec[k][0] for k in nats]


def xhtml_to_text(x):
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", "", x2)
    paras = []
    for b in re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2):
        t = re.sub(r"<[^>]+>", "", b).replace("&nbsp;", " ")
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return "\n\n".join(paras)


def next_index(out_dir):
    n = 0
    for f in (os.listdir(out_dir) if os.path.isdir(out_dir) else []):
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
    ap.add_argument("--first", default="backward", choices=["backward", "forward"],
                    help="先回卷还是先正向; 停在书尾时应选 backward 从头开始")
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

    stats = {"resp": 0, "docs": 0, "dup": 0, "fail": 0, "empty": 0}
    new_count = 0
    groups = []
    cur = None
    pending = {}        # requestId -> idx (收到响应头)
    finished = []       # 已完成加载的 requestId 队列(在主循环里读 body, 避免事件内阻塞死锁)
    import queue as _queue
    fin_q = _queue.Queue()

    def add_shard(idx, body):
        nonlocal cur
        now = time.time()
        # 按时间窗口归并: 同一章分片在 ~1s 内密集到达; 跨章之间有翻页间隔(>=pause)空隙。
        # 不再依赖 idx==0(实践表明 e_0 可能晚到, 不能作分组边界)。
        if cur is None or (now - cur["last"]) >= GROUP_GAP:
            cur = {"shards": {}, "start": now, "last": now, "sealed": False}
            groups.append(cur)
        cur["shards"][idx] = body
        cur["last"] = now

    def write_one(src_html, text):
        nonlocal new_count
        if len(text) < 20:
            return False
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        if h in hashes:
            stats["dup"] += 1
            return False
        idx = next_index(out_dir)
        html_path = os.path.join(out_dir, "%04d.html" % idx)
        txt_path = os.path.join(out_dir, "%04d.txt" % idx)
        try:
            with open(html_path, "w", encoding="utf-8", newline="") as f:
                f.write(src_html); f.flush(); os.fsync(f.fileno())
            with open(txt_path, "w", encoding="utf-8", newline="") as f:
                f.write(text); f.flush(); os.fsync(f.fileno())
        except Exception as e:
            print("  [write fail] %04d: %s" % (idx, str(e)[:60]))
            return False
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
            return False
        hashes.add(h)
        new_count += 1
        print("  [确认落盘] %04d.txt %6d字" % (idx, len(text)), flush=True)
        return True

    def flush_group(g):
        """把一组分片尽力写成正文, 失败也尽量靠硬拼兜底, 不丢内容"""
        parts = sorted(g["shards"].items())
        if not parts:
            return []
        src, order = best_join(parts)
        if not src:
            return []
        text = xhtml_to_text(src)
        if len(text) < 20:
            return []
        stats["docs"] += 1
        return [(0, len(text))] if write_one(src, text) else []

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

        def on_recv(evt):
            # cdp.on 回调收到的已是 params 本身
            try:
                url = evt["response"]["url"]
                rid = evt["requestId"]
            except Exception:
                return
            last = url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in url or "e_" not in last:
                return
            m = re.search(r"e_e?_(\d+)$", last) or re.search(r"e_(\d+)$", last)
            if m:
                pending[rid] = int(m.group(1))

        def on_fin(evt):
            # 事件内只入队, 绝不做阻塞 send; 真正的 getResponseBody 在主循环里执行
            try:
                rid = evt["requestId"]
            except Exception:
                return
            if rid in pending:
                fin_q.put(rid)

        cdp.on("Network.responseReceived", on_recv)
        cdp.on("Network.loadingFinished", on_fin)

        def drain_finished():
            while not fin_q.empty():
                try:
                    rid = fin_q.get_nowait()
                except Exception:
                    break
                idx = pending.pop(rid, None)
                if idx is None:
                    continue
                try:
                    res = cdp.send("Network.getResponseBody", {"requestId": rid})
                except Exception:
                    stats["fail"] += 1
                    continue
                body = res.get("body", "")
                if not body:
                    stats["empty"] += 1
                    stats["fail"] += 1
                    continue
                raw = base64.b64decode(body) if res.get("base64Encoded") else body.encode("latin1")
                if not raw:
                    stats["empty"] += 1
                    continue
                stats["resp"] += 1
                # DEBUG
                try:
                    d = decode_part(raw, 33)
                    dbg = "decoded_len=%s head=%r" % (len(d) if d else None, (d[:30] if d else None))
                except Exception as e:
                    dbg = "decode_err=%s" % str(e)[:40]
                print("  [shard] idx=%d b64enc=%s rawlen=%d head=%r | %s"
                      % (idx, res.get("base64Encoded"), len(raw), raw[:16], dbg), flush=True)
                add_shard(idx, raw)

        page.goto(cfg["reader"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)
        print("[start] 当前章节《%s》" % current_chapter(page))

        for _ in range(3):
            try: page.keyboard.press("ArrowRight")
            except Exception: pass
            time.sleep(args.pause)
            drain_finished()
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
                drain_finished()
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
                if press % 20 == 0:
                    try:
                        anchor = page.url().split("?k=")[-1][:22]
                    except Exception:
                        anchor = "?"
                    print("[%s 第%04d页] 锚点=%s | 《%s》 | 磁盘%d"
                          % (label, press, anchor, current_chapter(page), disk_n), flush=True)
                if idle and idle % 20 == 0:
                    print("   ...%s idle=%d resp=%d docs=%d fail=%d empty=%d"
                          % (label, idle, stats["resp"], stats["docs"], stats["fail"], stats["empty"]), flush=True)
                if idle >= args.idle:
                    print("[%s] 连续%d页无新内容,本阶段结束" % (label, idle))
                    break

    # 阅读器通常停在"上次阅读位置"(本书约85%); 先回卷到书首, 再从第一页正向慢读
    # ——既保证从头开始的正序抓取, 回卷过程本身也会把沿途章节顺带抓下来。
    if args.first == "backward":
        order = [("ArrowLeft", "回卷(当前位置→书首)"),
                 ("ArrowRight", "正向精读(书首→书尾)")]
    else:
        order = [("ArrowRight", "正向精读(书首→书尾)"),
                 ("ArrowLeft", "回卷(书尾→书首)")]
    for key, label in order:
        phase(key, label)

        print("[收尾] 强制结算残留组...")
        drain_finished()
        now = time.time()
        for g in groups:
            if not g["sealed"]:
                g["sealed"] = True
                flush_group(g)
        print("[done] 本次新增:%d | docs:%d fail:%d empty:%d dup:%d | 磁盘文件数:%d"
              % (new_count, stats["docs"], stats["fail"], stats["empty"], stats["dup"], next_index(out_dir)))
        try:
            b.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
