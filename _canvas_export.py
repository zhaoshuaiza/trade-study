#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canvas 全文导出 v2 —— 移植自 GitHub 2348 星方案 drunkdream/weread-exporter
核心: Hook HTMLCanvasElement.prototype.getContext -> 拦截 fillText ->
      按 (x,y) 与字号/颜色重组为 markdown (见 tools/weread-exporter-main/weread_exporter/hook.js)

v2 相对 v1 的关键修复 (2026-10-23):
  1. ⭐⭐ 章节污染: 阅读器会预载后续章节, 翻"下一页"会冲进下一章并在同一
     markdown 里继续累积 (002-版权信息.md 实测含到"引言"开头)。
     -> 导出后按 `## 标题` 行裁剪: 遇到下一章标题(或任何非本章标题)即截断;
        翻屏过程中看到下一章标题也立即停翻, 省掉 2/3 时间。
  2. `<sup>` 是阅读器的章节锚标记, 会把标题和正文首行粘在一起 -> 统一替换为换行。
  3. 自包含 Edge 生命周期: 9222 未监听则启动 fresh profile Edge, 结束时只杀
     监听 9222 的进程(taskkill /T), 不碰用户日常浏览器。
  4. 标题校验放宽: hook 没给出标题行(norm 后为空)时不再误杀整章。
  5. wordCount<=5 的空章(封面)直接跳过, 否则会落到下一章内容上。

章节地址: https://weread.qq.com/web/reader/{vid}k{wr_hash(chapterUid)}   (wr_hash 已本地校验 87/87)
"""
import argparse, json, os, re, sys, time, hashlib, socket, subprocess

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
HOOK_JS = r"E:/Work Buddy/tools/weread-exporter-main/weread_exporter/hook.js"

BOOKS = {
    "2015": {
        "vid": "33d32010813ab98e8g019623",
        "dir": os.path.join(ROOT, "raw", "distilled", "steenbarger-2015-zh"),
    },
    "2002": {
        "vid": "5ea329c0813abbcbeg01667b",
        "dir": os.path.join(ROOT, "raw", "distilled", "steenbarger-2002-zh"),
    },
}

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
EDGE_PROFILE = "E:/_edge_fresh"
DEBUG_PORT = 9222


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def wr_hash(s):
    """与原项目 utils.wr_hash 完全一致, 本地已校验 87/87 命中"""
    hash_str = md5(s)
    result = hash_str[:3] + "32" + hash_str[-2:]
    parts = []
    for i in range(0, len(s), 9):
        parts.append("%x" % int(s[i:min(i + 9, len(s))]))
    for i, it in enumerate(parts):
        n = "%x" % len(it)
        if len(n) == 1:
            n = "0" + n
        result += n + it
        if i < len(parts) - 1:
            result += "g"
    if len(result) < 20:
        result += hash_str[:20 - len(result)]
    result += md5(result)[:3]
    return result


def slug(t):
    t = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", t).strip()
    return t[:40] or "untitled"


def norm_t(s):
    """标题归一化: 截掉 <sup> 及其后正文, 去空白/括号/冒号/井号"""
    s = re.split(r"<", s or "")[0]
    return re.sub(r"[\s（）()【】\[\]：:#]", "", s)[:24]


# ---------------- Edge 生命周期 ----------------

def port_open(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False


def start_edge(port=DEBUG_PORT, profile=EDGE_PROFILE):
    exe = next((p for p in EDGE_PATHS if os.path.isfile(p)), None)
    if not exe:
        print("[err] 找不到 msedge.exe", flush=True)
        return False
    subprocess.Popen([exe, "--remote-debugging-port=%d" % port,
                      "--user-data-dir=" + profile, "about:blank"])
    for _ in range(40):
        if port_open(port):
            return True
        time.sleep(1)
    return False


def kill_edge(port=DEBUG_PORT):
    """只杀监听调试端口的 Edge 主进程(即 fresh profile), 不碰用户日常浏览器"""
    try:
        try:
            out = subprocess.run("netstat -ano", shell=True, capture_output=True,
                                 text=True, encoding="utf-8", errors="replace",
                                 timeout=30).stdout or ""
        except Exception:
            return 0
        pids = set()
        for line in out.splitlines():
            if (":%d" % port) not in line or "LISTENING" not in line:
                continue
            m = re.search(r"LISTENING\s+(\d+)\s*$", line)
            if m:
                pids.add(m.group(1))
        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/T", "/F"], capture_output=True)
        return len(pids)
    except Exception:
        return 0


# ---------------- 页面状态读取 ----------------

POLL_COMPLETE = "window.canvasContextHandler.data.complete;"
GET_MD = "window.canvasContextHandler.data.markdown;"

# 页面底部. readerFooter_button 在新版 DOM 里已不存在, 改为按按钮文本定位
JS_FIND_PAGE = """() => {
  const bs = Array.from(document.querySelectorAll('button'));
  const tx = bs.map(b => (b.innerText || '').trim());
  if (tx.indexOf('下一页') >= 0) return 'PAGE';
  if (tx.indexOf('下一章') >= 0) return 'CHAPTER';
  return 'NONE:' + tx.filter(Boolean).slice(0, 6).join('|');
}"""

JS_CLICK_NEXT = """() => {
  const bs = Array.from(document.querySelectorAll('button'));
  const b = bs.find(x => (x.innerText || '').trim() === '下一页');
  if (!b) return false;
  b.click();
  return true;
}"""

# 新版 DOM 里已无 div.chapterTitle; 标题只能从 hook markdown 的 ## 行取
JS_RENDERED_TITLE = ("() => {const W=window.canvasContextHandler;"
                     "const md=(W&&W.data.markdown)||'';"
                     "const m=md.match(/^##[ \\t]*(.+)$/m);"
                     "return m ? m[1].trim() : '';}")


def read_state(page):
    try:
        done = page.evaluate(POLL_COMPLETE)
    except Exception:
        return None, ""
    try:
        md = page.evaluate(GET_MD) or ""
    except Exception:
        md = ""
    return done, md


def wait_render(page, timeout=25):
    t0 = time.time()
    while time.time() - t0 < timeout:
        done, _ = read_state(page)
        if done:
            return True
        time.sleep(0.6)
    return False


def harvest_page(page, acc, prev):
    """累计当前屏; 返回新的 prev。同时兼容 markdown 累积 / 每屏重置两种行为"""
    _, md = read_state(page)
    if not md:
        return prev
    if prev and md.startswith(prev) and len(md) > len(prev):
        acc.append(md[len(prev):])
    elif md != prev:
        acc.append(md)
    return md


def find_heading_cut(md, expect_title, next_title):
    """⭐ 章节裁剪: 返回第一个'非本章标题'的 ## 行的行号(不含), 没有则 None。
    优先匹配下一章标题(精确); 下一章标题缺失时退化为'任何非本章标题'。"""
    ne, nn = norm_t(expect_title), norm_t(next_title)
    for i, ln in enumerate(md.split("\n")):
        m = re.match(r"^##\s+(.+)$", ln)
        if not m:
            continue
        t = norm_t(m.group(1))
        if not t:
            continue
        if nn and t == nn:
            return i
        if t != ne:
            return i
    return None


DEBUG = False
MP_GLOBAL = 200


def export_chapter(ctx, page, url_base, k, out_path, expect_title="",
                   next_title="", max_pages=MP_GLOBAL, pause=0.8):
    md_out = []
    try:  # 全程复用同一标签页, 避免 95 章反复开页把 Edge 拖崩
        page.bring_to_front()   # ⭐ 后台标签页不发 rAF -> Canvas 不入画 -> markdown 恒空
    except Exception:
        pass
    try:
        url = url_base + k  # url_base 已含分隔符('k' 或 '?k='), 勿重复拼接
        if DEBUG:
            print("  [dbg] goto %s" % url, flush=True)
        # ⭐ 先落地空白页再进章节: SPA 复用同一 document 时会残留上一章渲染结果
        try:
            page.goto("about:blank", timeout=20000)
            time.sleep(1.5)
        except Exception:
            pass
        page.goto(url, timeout=90000, wait_until="load")
        time.sleep(3.0)   # 慢速: 给 Canvas 首屏绘制留出时间
        if DEBUG:
            print("  [dbg] goto-done url=%s title=%s" % (page.url[:80], page.title()[:40]),
                  flush=True)
        # 等待 hook 就位
        t0 = time.time()
        while time.time() - t0 < 25:
            try:
                if page.evaluate("typeof window.canvasContextHandler !== 'undefined'"):
                    break
            except Exception:
                pass
            time.sleep(0.5)
        if DEBUG:
            try:
                st = page.evaluate(
                    "() => {const W=window.canvasContextHandler;"
                    "return W ? [W.data.complete, (W.data.markdown||'').length] : 'NOHOOK';}")
                print("  [dbg] hook状态=%s (等待%.1fs)" % (st, time.time() - t0), flush=True)
            except Exception as e:
                print("  [dbg] hook状态读取失败: %s" % str(e)[:80], flush=True)

        wait_render(page, timeout=45)
        # ⭐ 校验渲染出来的章节标题是否真是目标章; 没有标题信息(norm 为空)时放行
        got = ""
        for attempt in (1, 2, 3):
            try:
                got = page.evaluate(JS_RENDERED_TITLE) or ""
            except Exception:
                got = ""
            if (not expect_title) or (not norm_t(got)) or norm_t(got) == norm_t(expect_title):
                break
            if DEBUG:
                print("  [dbg] 标题不符(<%s> != <%s>), 第%d次慢等重载"
                      % (got[:16], expect_title[:16], attempt), flush=True)
            time.sleep(4.0)          # 先给页面时间, 别急着判死
            try:
                got = page.evaluate(JS_RENDERED_TITLE) or ""
            except Exception:
                got = ""
            if norm_t(got) == norm_t(expect_title):
                break
            try:
                page.goto("about:blank", timeout=20000)
                time.sleep(1.5)
                page.goto(url, timeout=90000, wait_until="load")
                time.sleep(3.0)
                wait_render(page, timeout=45)
            except Exception:
                break
        if expect_title and norm_t(got) and norm_t(got) != norm_t(expect_title):
            print("  [warn] 章节对不上: 期望<%s> 实得<%s> -> 跳过, 不落盘"
                  % (expect_title[:20], got[:20]), flush=True)
            return 0, False
        prev = ""

        screens = 0
        stall = 0
        while screens < max_pages:
            prev = harvest_page(page, md_out, prev)
            # ⭐ 早停: markdown 里已出现下一章(或任何外章)标题 -> 本章采完, 别再翻
            if next_title or expect_title:
                _, md_now = read_state(page)
                if md_now and find_heading_cut(md_now, expect_title, next_title) is not None:
                    if DEBUG:
                        print("    [dbg] 早停: 已见下一章标题", flush=True)
                    # 标题可能比正文先画出来: 再多收几轮, 防止截短本章正文
                    for _ in range(3):
                        time.sleep(1.5)
                        prev = harvest_page(page, md_out, prev)
                    break
            try:
                state = page.evaluate(JS_FIND_PAGE)
            except Exception:
                break
            if state != "PAGE":
                if DEBUG:
                    print("    [dbg] 到底, state=%s" % str(state)[:60], flush=True)
                if state.startswith("登录"):
                    print("  !! 需要登录", flush=True)
                break
            time.sleep(2.0)          # ⭐ 慢速: 翻屏前先等前一屏彻底画完
            try:
                if not page.evaluate(JS_CLICK_NEXT):
                    break
            except Exception:
                break
            screens += 1
            # ⭐ 不再死等 complete: 只要 markdown 变长就说明这一屏渲染完了
            t1 = time.time()
            grew = False
            while time.time() - t1 < (20 if screens == 1 else 14):
                time.sleep(0.8)
                _, md_now = read_state(page)
                if len(md_now) > len(prev):
                    grew = True
                    break
            time.sleep(1.0)          # ⭐ 慢速: 翻屏后再稳一稳
            if not grew:
                stall += 1
                if stall >= 3:      # 连着 3 屏都没新内容 -> 本章到底
                    break
            else:
                stall = 0
            if DEBUG and screens % 5 == 0:
                print("    [dbg] 第%d屏 累计=%d字" %
                      (screens, sum(len(x) for x in md_out)), flush=True)

        prev = harvest_page(page, md_out, prev)
        text = "\n".join(md_out).strip()
        # ⭐ 裁剪掉冲进来的下一章内容
        cut = find_heading_cut(text, expect_title, next_title)
        if cut is not None:
            text = "\n".join(text.split("\n")[:cut]).strip()
        # <sup> 是章节锚标记, 会把标题和正文首行粘住 -> 换成换行
        text = text.replace("<sup>", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        if not text:
            return 0, False
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        return len(text), True
    finally:
        try:  # 复用页面: 只清累积的 markdown, 不关标签页
            page.evaluate("window.canvasContextHandler.clearCanvasCache();")
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--only", default="", help="只导某些 uid, 逗号分隔")
    ap.add_argument("--pause", type=float, default=0.8)
    ap.add_argument("--urlmode", default="slash", choices=["slash", "query"],
                    help="slash=/reader/VID k HASH ; query=/reader/VID?k=HASH")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--minutes", type=float, default=0,
                    help="到时干净退出(分钟), 0=不限; 前台分块用, 避免被环境回收")
    ap.add_argument("--range", default="", help="只导某段章节(1基位置), 如 20-47")
    ap.add_argument("--port", type=int, default=DEBUG_PORT)
    ap.add_argument("--profile", default=EDGE_PROFILE)
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--maxpages", type=int, default=200)
    args = ap.parse_args()
    global DEBUG
    DEBUG = args.debug
    global MP_GLOBAL
    MP_GLOBAL = args.maxpages

    cfg = BOOKS[args.book]
    chap_path = os.path.join(cfg["dir"], "_chapters.json")
    full = json.load(open(chap_path, encoding="utf-8"))
    title_by_uid = {str(c["chapterUid"]): c.get("title", "") for c in full}
    uid_order = [str(c["chapterUid"]) for c in full]
    chapters = full
    if args.only:
        want = set(x.strip() for x in args.only.split(","))
        chapters = [c for c in full if str(c["chapterUid"]) in want]
    if args.range:
        a, b = (int(x) for x in args.range.split("-"))
        chapters = [c for c in chapters
                    if a <= uid_order.index(str(c["chapterUid"])) + 1 <= b]
    out_root = os.path.join(cfg["dir"], "canvas")
    os.makedirs(out_root, exist_ok=True)

    root = "https://weread.qq.com/web/reader/" + cfg["vid"]
    url_base = root + ("?k=" if args.urlmode == "query" else "k")

    print("[start] book=%s 章节=%d url=%s..." % (args.book, len(chapters), url_base[:60]),
          flush=True)

    # ⭐ hook.js 在 Proxy 的 get 里对每个属性读取都 console.log(name, ...),
    #    super-heavy: 会把 CDP 通道打满, 令后续 page.evaluate 永久阻塞。
    #    因此把整段 hook 包进 IIFE, 内部用一个 noop console 顶掉日志。
    hook_src = ";(function(){\nvar console={log:function(){},warn:function(){},"
    hook_src += "error:function(){},info:function(){},debug:function(){}};\n"
    hook_src += open(HOOK_JS, encoding="utf-8").read()
    # hook.js 顶层用 `let`, 闭包外不可见, 需在末尾显式挂到 window
    hook_src += "\nwindow.canvasContextHandler = canvasContextHandler;\n})();"
    total_chars = 0
    ok_n = 0
    idx_map = []
    own_edge = False
    with sync_playwright() as pw:
        if port_open(args.port):
            print("[info] %d 已有监听, 复用现有 Edge" % args.port, flush=True)
        else:
            own_edge = start_edge(args.port, args.profile)
            print("[info] 启动 fresh Edge port=%d profile=%s (own=%s)"
                  % (args.port, args.profile, own_edge), flush=True)
            if not own_edge:
                print("[err] Edge 启动失败, 退出", flush=True)
                return
        try:
            b = pw.chromium.connect_over_cdp("http://127.0.0.1:%d" % args.port)
            ctx = b.contexts[0]
            ctx.add_init_script(hook_src)
            shared = ctx.new_page()
            try:
                shared.bring_to_front()
            except Exception:
                pass
            t_start = time.time()
            for i, ch in enumerate(chapters, 1):
                uid = str(ch["chapterUid"])
                title = ch.get("title", "")
                wc = int(ch.get("wordCount", 0) or 0)
                if wc <= 5:
                    print("[skip] %03d %-30s wordCount=%d 空章" % (i, title[:30], wc),
                          flush=True)
                    continue
                # ⭐ 时限检查放在开跑新章之前, 并留1分钟余量:
                #    长章(如6285字)单章可跑2分钟, 放到章后检查会被硬超时SIGTERM
                if args.minutes and (time.time() - t_start) > (args.minutes - 1.0) * 60:
                    print("[stop] 已达 %.1f 分钟预算(含1分钟余量), 干净退出 (进度已落盘, 重跑自动续)"
                          % args.minutes, flush=True)
                    break
                pos = uid_order.index(uid)
                next_title = title_by_uid[uid_order[pos + 1]] if pos + 1 < len(uid_order) else ""
                k = wr_hash(uid)
                # ⭐ 文件名序号用全文章节位置(pos+1), 不能用过滤后列表的 i
                fname = "%03d-%s.md" % (pos + 1, slug(title))
                out = os.path.join(out_root, fname)
                if os.path.isfile(out) and os.path.getsize(out) > 30:
                    print("[skip] %s 已存在 %d字节" % (fname, os.path.getsize(out)), flush=True)
                    continue
                n, ok = export_chapter(ctx, shared, url_base, k, out,
                                       expect_title=title, next_title=next_title,
                                       pause=args.pause)
                if ok:
                    total_chars += n
                    ok_n += 1
                    idx_map.append((os.path.basename(out), title, uid, n))
                    print("[%3d/%3d] %-30s %6d字  (累计%d)" %
                          (pos + 1, len(full), title[:30], n, total_chars), flush=True)
                else:
                    print("[%3d/%3d] %-30s !! 无内容" % (pos + 1, len(full), title[:30]), flush=True)
                    idx_map.append((os.path.basename(out), title, uid, 0))
                if args.limit and i >= args.limit:
                    break
                time.sleep(2.5)   # ⭐ 慢速: 章与章之间留出人工阅读般的间隔
            try:
                b.close()
            except Exception:
                pass
        finally:
            if own_edge:
                time.sleep(2)
                n = kill_edge(args.port)
                print("[info] 关闭 fresh Edge port=%d (kill %d)" % (args.port, n), flush=True)

    json.dump(idx_map, open(os.path.join(out_root, "_index.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[done] 成功%d章/%d, 共%d字, 耗时%.1f分钟" %
          (ok_n, len(chapters), total_chars, (time.time() - t_start) / 60), flush=True)


if __name__ == "__main__":
    main()
