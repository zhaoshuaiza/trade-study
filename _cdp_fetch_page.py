#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐页确认式抓取: 每按一次方向键,先确认本页是否真的产生了新内容,再继续。

python _cdp_fetch_page.py --book 2015 [--maxpress N] [--idle M] [--key ArrowRight]
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


def toc_coverage(out_dir):
    """返回目录命中率,便于每页确认进度。"""
    try:
        toc = json.load(open(os.path.join(out_dir, "_toc.json"), encoding="utf-8"))
    except Exception:
        return None
    import glob
    txt = ""
    for f in sorted(glob.glob(os.path.join(out_dir, "[0-9][0-9][0-9][0-9].txt"))):
        txt += open(f, encoding="utf-8").read() + "\n"
    hit = 0
    for t in toc:
        k = re.sub(r"[（(].*?[)）]", "", t.strip()).strip()
        if len(k) >= 2 and k in txt:
            hit += 1
    return hit, len(toc)


def current_chapter(page):
    """读取当前所在章节名(body 第 5 行即阅读器章节标题)。"""
    try:
        t = page.evaluate("() => (document.body.innerText||'')").split("\n")
        return t[4].strip() if len(t) > 4 else "?"
    except Exception:
        return "?"


def go_home(page, maxbatch=10, perbatch=400):
    """连按 ArrowLeft 一路退到书的最前面(连续两次不再变化为止)。"""
    prev, same = None, 0
    for i in range(maxbatch):
        for _ in range(perbatch):
            try:
                page.keyboard.press("ArrowLeft")
            except Exception:
                pass
        time.sleep(1.4)
        c = current_chapter(page)
        print("  [回退] 批次%d -> %s" % (i + 1, c))
        if c == prev:
            same += 1
            if same >= 2:
                print("  [回退] 已退到最前:", c)
                break
        else:
            same = 0
        prev = c
        if c in ("封面", "扉页", "版权信息"):
            print("  [回退] 到达书首:", c)
            break
    # 向右翻一页,让 URL 锚定到书首章节的 id(供 reload 使用)
    for _ in range(2):
        try:
            page.keyboard.press("ArrowRight")
        except Exception:
            pass
        time.sleep(1.5)
    time.sleep(4)  # 给阅读进度同步留时间
    return page.url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--key", default="ArrowRight", choices=["ArrowRight", "ArrowLeft"])
    ap.add_argument("--maxpress", type=int, default=600)
    ap.add_argument("--idle", type=int, default=25)
    ap.add_argument("--noreload", action="store_true")
    ap.add_argument("--pause", type=float, default=3.0, help="每页按键后等待秒数,太快会被取消")
    ap.add_argument("--home", action="store_true", help="先连按左键退回书首并清本地缓存")
    args = ap.parse_args()

    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)

    hashes = set()
    anchor_path = os.path.join(out_dir, "_anchors.json")
    anchor_map = {}
    if os.path.exists(anchor_path):
        try:
            anchor_map = json.load(open(anchor_path, encoding="utf-8"))
        except Exception:
            anchor_map = {}
    for f in os.listdir(out_dir):
        if re.match(r"\d+\.txt$", f):
            try:
                with open(os.path.join(out_dir, f), encoding="utf-8") as fh:
                    hashes.add(hashlib.md5(fh.read().encode("utf-8")).hexdigest())
            except Exception:
                pass
    print("[init] existing chunks:", len(hashes))
    cov = toc_coverage(out_dir)
    if cov:
        print("[init] 目录覆盖: %d/%d" % cov)

    new_count = 0
    anchor_path = os.path.join(out_dir, "_anchors.json")
    anchor_map = {}
    if os.path.exists(anchor_path):
        try:
            anchor_map = json.load(open(anchor_path, encoding="utf-8"))
        except Exception:
            anchor_map = {}

    def record_anchor(chap):
        """记录 URL 锚点 -> 章节名 的映射,便于后续定点回到任意已知章节。"""
        try:
            m = re.search(r"k([0-9a-f]{20,})", page.url)
        except Exception:
            return
        if m and m.group(1) not in anchor_map:
            anchor_map[m.group(1)] = chap
            try:
                with open(anchor_path, "w", encoding="utf-8") as fh:
                    json.dump(anchor_map, fh, ensure_ascii=False, indent=0)
            except Exception:
                pass

    cur_group = []       # 正在收集的一组(以 e_0 开头)
    ready_groups = []    # 已被下一个 e_0 封口、可组装的组
    last_resp = [time.time()]
    stats = {"resp": 0, "docs": 0, "dup": 0, "fail": 0}

    def flush(group):
        """返回本批成功落盘并通过回读校验的 [(idx, 字数)] 列表。"""
        nonlocal new_count
        saved = []
        parts = sorted(group, key=lambda x: x[1])
        cand = [(i, b) for _, i, b in parts
                if not any(b[33:].decode("latin1", "ignore").startswith(p) for p in CSS_START)]
        if not cand:
            return saved
        docs, order = assemble(cand)
        if not docs:
            stats["fail"] += 1
            return saved
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
            # 1) 写入 + fsync 强制落盘
            try:
                # newline="" 禁止 \n -> \r\n 转换,保证回读 md5 与内存一致
                with open(html_path, "w", encoding="utf-8", newline="") as f:
                    f.write(d)
                    f.flush()
                    os.fsync(f.fileno())
                with open(txt_path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
                    f.flush()
                    os.fsync(f.fileno())
            except Exception as e:
                print("  [write fail] %04d: %s" % (idx, str(e)[:60]))
                continue
            # 2) 回读校验: 文件存在 + 字节数 + md5 三项全对才算确认
            ok = False
            try:
                with open(txt_path, "rb") as f:
                    raw = f.read()
                rb = raw.decode("utf-8", "ignore")
                size_ok = os.path.getsize(txt_path) > 0 and os.path.getsize(html_path) > 0
                md5_ok = hashlib.md5(rb.encode("utf-8")).hexdigest() == h
                len_ok = len(rb) == len(text)
                ok = size_ok and md5_ok and len_ok
            except Exception as e:
                print("  [verify fail] %04d: %s" % (idx, str(e)[:60]))
            if not ok:
                stats["fail"] += 1
                print("  [verify BAD] %04d 校验未通过, 不计入进度" % idx)
                continue
            hashes.add(h)
            new_count += 1
            saved.append((idx, len(text)))
            print("  [已确认落盘] %04d.txt %6d字  md5校验通过" % (idx, len(text)))
        return saved

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
            # ⭐关键: 必须清"浏览器级" HTTP 缓存,否则已请求过的章节不再走网络
            cdp.send("Network.enable")
            cdp.send("Network.clearBrowserCache")
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            print("[cdp] browser cache cleared + cache disabled")
        except Exception as e:
            cdp = None
            print("[cdp] fail", str(e)[:70])

        start_url = cfg["reader"]
        if args.home:
            print("[home] 正在连按左键退回书首...")
            start_url = go_home(page) or cfg["reader"]
            print("[home] 锚点 URL:", start_url[-40:])
            # 清除本地内容缓存(保留 cookie/登录态),迫使重新向服务器请求
            if cdp:
                cleared = []
                for st in ["indexeddb", "local_storage", "cache_storage", "service_workers"]:
                    try:
                        cdp.send("Storage.clearDataForOrigin",
                                 {"origin": "https://weread.qq.com", "storageTypes": st})
                        cleared.append(st)
                    except Exception:
                        pass
                print("[home] 已清本地缓存:", cleared)

        def on_response(resp):
            """以 e_0(起始分片) 为锚点切分组:新 e_0 到达即代表上一组成型。

            这样天然保证每组完整,避免并发批次导致 idx 交错而拼装失败。
            """
            last = resp.url.rstrip("/").split("/")[-1]
            if "/web/book/chapter/" not in resp.url or not last.startswith("e_"):
                return
            try:
                idx = int(last.split("_")[1])
                body = resp.body()
            except Exception:
                return
            stats["resp"] += 1
            last_resp[0] = time.time()
            item = (time.time(), idx, body)
            if idx == 0:
                if cur_group:
                    ready_groups.append(cur_group)
                cur_group[:] = [item]
            else:
                cur_group.append(item)

        page.on("response", on_response)
        if args.home or not args.noreload:
            try:
                page.goto(start_url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(10)
                print("[reload] ok -> 当前章节:", current_chapter(page))
            except Exception as e:
                print("[reload] fail", str(e)[:70])

        def is_css(bd):
            try:
                return bd[33:].decode("latin1", "ignore").startswith("Lyoq")
            except Exception:
                return False

        def group_ready(g):
            """组可用条件: 含起始分片(<?xml) 且有效成员 >= 3 ;残缺则继续等待。"""
            has_head = False
            for _, _i, bd in g:
                r = decode_part(bd)
                if r and r[:5] == b"<?xml":
                    has_head = True
                    break
            valid = sum(0 if is_css(bd) else 1 for _, _i, bd in g)
            if has_head and valid >= 3:
                return True
            # 兜底:首片到达超过 30 秒仍不齐,再试一次
            return (time.time() - g[0][0]) > 30.0

        def settle(force=False):
            """结算已成型(被下一个 e_0 封口)的分组,返回本轮落盘确认结果。

            对组内最后一片到达不足 1.5 秒的组再等一等,给迟到的分片留余量。
            """
            out = []
            while ready_groups:
                g = ready_groups[0]
                last_arrive = max(t for t, _i, _b in g)
                if not force and (time.time() - last_arrive) < 1.5:
                    break
                ready_groups.pop(0)
                out.extend(flush(g))
            if force and cur_group:
                g = list(cur_group)
                cur_group[:] = []
                out.extend(flush(g))
            return out

        # ⭐ 预热: goto 后阅读器翻页控制器往往未激活,直接按方向键会 0 请求。
        #    先按几次 ArrowRight 触发至少一章加载,把控制器激活,之后正/反向都可靠。
        #    (用户已手动翻到首页并激活时,少量预热也无害——这几章同样会被拦截落盘)
        print("[activate] 预热翻页控制器(先 ArrowRight 几次)...")
        for _ in range(3):
            try:
                page.keyboard.press("ArrowRight")
            except Exception:
                pass
            time.sleep(args.pause)
        settle()

        idle = 0
        for press in range(args.maxpress):
            before = new_count
            resp_before = stats["resp"]
            # --- 步骤 1: 翻一页 ---
            try:
                page.keyboard.press(args.key)
            except Exception as e:
                print("[%04d] 按键失败: %s" % (press, str(e)[:60]))
            # --- 步骤 2: 慢速等待本页内容到达 (太快会被取消) ---
            time.sleep(args.pause)
            # --- 步骤 3: 落盘 + 回读校验 ---
            saved_pages = settle()
            disk_n = next_index(out_dir)
            got_new = new_count > before
            got_resp = stats["resp"] > resp_before
            # --- 步骤 4: 确认后才进入下一页 ---
            chap = current_chapter(page)
            record_anchor(chap)
            if saved_pages:
                idle = 0
                detail = ", ".join(["%04d(%d字)" % (i, n) for i, n in saved_pages])
                print("[第%04d页] ✓ 已落盘 %d 段(%s) | 现读《%s》 | 磁盘共%d文件"
                      % (press, len(saved_pages), detail, chap, disk_n))
            elif got_resp:
                # ⭐ 有请求但只是重复(已抓过的内容被重读): 阅读器仍在前进,不算卡住。
                #    只有"完全无请求"才累计 idle —— 那样才是真正到了书尾。
                idle = 0
                print("[第%04d页] ~ 重读已抓内容(重复%d) | 现读《%s》 | 磁盘共%d文件"
                      % (press, stats["dup"], chap, disk_n))
            else:
                idle += 1
                print("[第%04d页] . 本页无新请求 | 现读《%s》 | idle=%d | 磁盘共%d文件"
                      % (press, chap, idle, disk_n))
                # 无响应时给更长恢复时间,避免继续猛按加剧限流
                if idle % 10 == 0:
                    print("   ...冷却 5 秒")
                    time.sleep(5)
            if idle and idle % 10 == 0:
                cov = toc_coverage(out_dir)
                print("   >>> 目录覆盖: %s" % (("%d/%d" % cov) if cov else "?"))
            if idle >= args.idle:
                print("[end] 连续 %d 页无新内容,停止" % idle)
                break
            if press and press % 50 == 0:
                cov = toc_coverage(out_dir)
                print("   >>> 进度: 已翻 %d 页, 本次新增 %d 段, 目录覆盖 %s"
                      % (press, new_count, ("%d/%d" % cov) if cov else "?"))

        # 收尾: 强制结算残留的分片
        tail_saved = settle(force=True)
        if tail_saved:
            print("[收尾] 补充落盘 %d 段: %s"
                  % (len(tail_saved), ", ".join(["%04d(%d字)" % s for s in tail_saved])))

        cov = toc_coverage(out_dir)
        print("[done] 磁盘文件数:", next_index(out_dir), "| 本次新增:", new_count,
              "| 目录覆盖:", ("%d/%d" % cov) if cov else "?", "| stats:", stats)
        b.close()


if __name__ == "__main__":
    main()
