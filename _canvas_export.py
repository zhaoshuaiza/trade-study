#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canvas 全文导出 v3 —— 移植自 GitHub 2348 星方案 drunkdream/weread-exporter
核心: Hook HTMLCanvasElement.prototype.getContext -> 拦截 fillText ->
      按 (x,y) 与字号/颜色重组为 markdown (见 tools/weread-exporter-main/weread_exporter/hook.js)

v3 相对 v2 的关键修复 (2026-10-23):
  1. ⭐⭐⭐ 章节裁剪误杀: 2002 书章内有 `## 2.1 无意识的欲望…` 节标题,
     2015 书 uid89/90 章内有 `## 最佳实践#1…` 节标题, v2 把它们当"下一章标题"
     整章切掉(实测 2002 第1-7章+附录只剩标题行, 2015 有4章被截断)。
     -> v3: 只匹配**全书目录里的章标题**(归一化集合), 节标题一律放行。
  2. ⭐ 长章硬超时: 2002第7章43580字约115屏, 常速约12分钟 > 10分钟前台上限,
     被 SIGTERM 连章带内容一起没。-> 新增 --fast(翻屏1.0s/0.5s) + .part 增量落盘,
     每屏都写 part 文件, 被杀也能 salvage。
  3. 新增 --force: 重导已存在但截断的章节(审计出的坏章)。
  4. v2 其余保留: Edge 自起停(只杀监听调试端口的进程)/ 章节预载污染裁剪 /
     <sup>换行 / 空章跳过 / 时限按章节字数估算。

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
    """标题归一化: 截掉 <sup> 及其后正文, 去空白/全角空格/括号/冒号/井号"""
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


def wait_screen(page, prev, timeout=14.0, poll=0.6, stable_n=3):
    """⭐ 等新屏画完(替代v2的长度增长判断):
    hook 每屏 clearRect 后重建 markdown(见 hook.js clearCanvasCache),
    新屏全文可能比旧屏更短 -> 长度增长永远为假 -> 假停滞截断(实测012章被切)。
    正确信号: markdown 非空且与上一屏不同, 且连续 stable_n 次读数稳定
    (hook 自己的 complete 标志在末次 fillText 后 1s 置位, 稳定窗需大于它)。"""
    t0 = time.time()
    last = ""
    stable = 0
    while time.time() - t0 < timeout:
        time.sleep(poll)
        _, md = read_state(page)
        if not md or md == prev:
            last = ""
            stable = 0
            continue
        if md == last:
            stable += 1
            if stable >= stable_n:
                return True
        else:
            stable = 0
            last = md
    return False


def find_heading_cut(md, expect_title, toc_norms):
    """⭐ 章节裁剪: 返回第一个'其他章的目录标题'的 ## 行的行号(不含), 没有则 None。
    只匹配全书目录里的章标题 —— 章内节标题(如 2.1 xxx / 最佳实践#1)一律放行，
    这是 v2 把 2002 第1-7章切成只剩标题的根因。"""
    ne = norm_t(expect_title)
    for i, ln in enumerate(md.split("\n")):
        m = re.match(r"^#{2,}\s+(.+)$", ln)
        if not m:
            continue
        t = norm_t(m.group(1))
        if not t or t == ne:
            continue
        if t in toc_norms:      # 是全书另一章的标题 -> 本章已结束
            return i
    return None


DEBUG = False
MP_GLOBAL = 200


def export_chapter(ctx, page, url_base, k, out_path, expect_title="",
                   toc_norms=frozenset(), decoy_k="", max_pages=MP_GLOBAL, pace="normal"):
    md_out = []
    part_path = out_path + ".part"
    if pace == "fast":
        pre_s, post_s, poll_s, settle_n, settle_s, stable_n = 1.0, 0.5, 0.5, 2, 1.0, 3
    else:
        pre_s, post_s, poll_s, settle_n, settle_s, stable_n = 2.0, 1.0, 0.8, 3, 1.5, 3

    def finalize():
        text = "\n".join(md_out).strip()
        cut = find_heading_cut(text, expect_title, toc_norms)
        if cut is not None:
            text = "\n".join(text.split("\n")[:cut]).strip()
        text = text.replace("<sup>", "\n")          # 章节锚标记粘住标题和正文首行
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        # ⭐ 章首补标题行: 诱饵跳转时阅读器常常不渲染章标题(只渲染正文)
        m = re.match(r"^#{2,}\s+(.+)$", text, re.M)
        first_t = norm_t(m.group(1)) if m else ""
        if expect_title and first_t != norm_t(expect_title):
            text = "## %s\n\n%s" % (expect_title, text)
        return text

    try:  # 全程复用同一标签页, 避免 95 章反复开页把 Edge 拖崩
        page.bring_to_front()   # ⭐ 后台标签页不发 rAF -> Canvas 不入画 -> markdown 恒空
    except Exception:
        pass
    try:
        if os.path.isfile(part_path):     # 上次被杀的残尸, 重来
            os.remove(part_path)
        url = url_base + k  # url_base 已含分隔符('k' 或 '?k='), 勿重复拼接
        decoy_url = (url_base + decoy_k) if decoy_k else ""
        if DEBUG:
            print("  [dbg] goto %s" % url, flush=True)
        # ⭐⭐ 诱饵跳转: 阅读器会恢复服务器同步的阅读位置, 当目标章正是当前所在章时
        #    k哈希跳转变空转(实测重导2002第2章落在章中段, 丢开头两屏)。
        #    先跳别章把位置挪走, 再跳目标章 -> 稳定落在章首。
        landed = False
        for attempt in (1, 2):
            try:
                page.goto("about:blank", timeout=20000)
                time.sleep(1.2)
            except Exception:
                pass
            if decoy_url:
                try:
                    page.goto(decoy_url, timeout=90000, wait_until="load")
                    time.sleep(5.0)   # 等诱饵章渲染+位置同步
                except Exception:
                    pass
            try:
                page.goto(url, timeout=90000, wait_until="load")
            except Exception as e:
                print("  [warn] goto失败: %s" % str(e)[:60], flush=True)
                continue
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
            # ⭐ 落点校验: 首屏标题是"别的章的目录标题"才算落错;
            #    空标题/本章标题/节标题(如2.1)都放行(诱饵跳转时常不渲染章标题)
            try:
                got = page.evaluate(JS_RENDERED_TITLE) or ""
            except Exception:
                got = ""
            g = norm_t(got)
            if (not expect_title) or (not g) or g == norm_t(expect_title) or (g not in toc_norms):
                landed = True
                break
            print("  [warn] 落点存疑(首屏标题<%s>), 第%d次重跳" % (got[:20], attempt), flush=True)
            time.sleep(3.0)
        if not landed:
            print("  [warn] 章节对不上: 期望<%s> -> 跳过, 不落盘" % expect_title[:20], flush=True)
            return 0, False, "land-mismatch"
        prev = ""

        screens = 0
        stall = 0
        end_reason = "unknown"
        while screens < max_pages:
            prev = harvest_page(page, md_out, prev)
            # ⭐ .part 增量落盘: 长章被 SIGTERM 也能 salvage 已抓屏数
            try:
                with open(part_path, "w", encoding="utf-8", newline="") as f:
                    f.write(finalize())
            except Exception:
                pass
            # ⭐ 早停: markdown 里已出现其他章的目录标题 -> 本章采完, 别再翻
            if toc_norms:
                _, md_now = read_state(page)
                if md_now and find_heading_cut(md_now, expect_title, toc_norms) is not None:
                    if DEBUG:
                        print("    [dbg] 早停: 已见下一章标题", flush=True)
                    # 标题可能比正文先画出来: 再多收几轮, 防止截短本章正文
                    for _ in range(settle_n):
                        time.sleep(settle_s)
                        prev = harvest_page(page, md_out, prev)
                    end_reason = "next-heading"
                    break
            try:
                state = page.evaluate(JS_FIND_PAGE)
            except Exception:
                end_reason = "page-error"
                break
            if state != "PAGE":
                if DEBUG:
                    print("    [dbg] 到底, state=%s" % str(state)[:60], flush=True)
                if state.startswith("登录"):
                    print("  !! 需要登录", flush=True)
                end_reason = "btn:" + str(state)[:24]
                break
            time.sleep(pre_s)          # 翻屏前先等前一屏彻底画完
            try:
                if not page.evaluate(JS_CLICK_NEXT):
                    end_reason = "click-failed"
                    break
            except Exception:
                end_reason = "click-error"
                break
            screens += 1
            # ⭐ 不再死等 complete(首屏之后恒真), 改用稳定读数判断本屏画完
            if wait_screen(page, prev, timeout=(20 if screens == 1 else 14),
                           poll=poll_s, stable_n=stable_n):
                stall = 0
            else:
                stall += 1
                if stall >= 3:      # 连着 3 屏都没稳定新内容 -> 本章到底
                    end_reason = "stall"
                    break
            if DEBUG and screens % 5 == 0:
                print("    [dbg] 第%d屏 累计=%d字" %
                      (screens, sum(len(x) for x in md_out)), flush=True)
        else:
            end_reason = "maxpages"

        prev = harvest_page(page, md_out, prev)
        text = finalize()
        if not text:
            if os.path.isfile(part_path):
                os.remove(part_path)
            return 0, False, "no-content"
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        if os.path.isfile(part_path):
            os.remove(part_path)
        return len(text), True, end_reason
    finally:
        try:  # 复用页面: 只清累积的 markdown, 不关标签页
            page.evaluate("window.canvasContextHandler.clearCanvasCache();")
        except Exception:
            pass


# ==================== v4: 回退定位 + 正向采收 ====================
# v3 的两个致命问题(2026-10-24 实测定位):
#  1. 诱饵跳转(连续两次 goto)会把阅读器翻页状态搞坏 -> 每章只翻 4 屏就 stall。
#     v4 改为单次 goto, 实测可连续翻 22 屏不 stall。
#  2. 阅读器会恢复"服务器同步的本章阅读位置"(实测第21章 pr=99, 即落在章末),
#     k哈希跳转无法覆盖。v4 改为: 落地后先点"上一页"回退到本章标题出现(章首),
#     再从章首正向采到章末。全程可信点击(button.renderTarget_pager_button)。
#  3. 千万不要 mock hera/sentry/river 遥测: 进度同步依赖这些上报,
#     mock 掉之后 reload 会回退到旧位置(v6 实测)。

NEXT_SEL = 'button.renderTarget_pager_button:has-text("下一页")'
PREV_SEL = 'button.renderTarget_pager_button:has-text("上一页")'

# ⭐ 当前章名: 阅读器顶部栏把章名渲染在 body.innerText 的"我的书架"下一行
#    (实测 body 首部: 微信读书书城 / 书名 / 首页 / 我的书架 / <章名> / 上一页 / 下一页)
#    回退时用它判断是否已离开本章 —— 回退屏不渲染章标题, 靠 md 里的 ## 行判不了。
# ⭐⭐ 视口必须是单栏宽(<=800): 宽视口下阅读器用 2 个 canvas 做双页跨页排版,
#    hook 每次 clearRect 只留下最后画的那一页 -> 每屏丢一半正文(实测宽视口每屏
#    406~446字, 窄视口 554~685字; 截图可见两栏而 md 只剩一栏)。
VIEWPORT = {"width": 700, "height": 900}

JS_CUR_CHAPTER = """() => {
  const t = (document.body.innerText || '').split('\\n').map(s => s.trim()).filter(Boolean);
  const i = t.indexOf('我的书架');
  return (i >= 0 && t[i + 1]) ? t[i + 1] : '';
}"""


def slice_chapter(text, expect_title, toc_norms):
    """⭐ 精确切片: 保留'本章标题行'起、到'下一个目录标题行'前的正文。
    回退过头时正文会带上一章尾巴, 正向过头会带下一章开头, 两端都切掉。"""
    lines = text.split("\n")
    ne = norm_t(expect_title)
    start, end = 0, len(lines)
    for i, ln in enumerate(lines):
        m = re.match(r"^#{2,}\s+(.+)$", ln)
        if m and norm_t(m.group(1)) == ne:
            start = i
            break
    for i in range(start + 1, len(lines)):
        m = re.match(r"^#{2,}\s+(.+)$", lines[i])
        if m:
            t = norm_t(m.group(1))
            if t and t != ne and t in toc_norms:
                end = i
                break
    return "\n".join(lines[start:end]).strip()


def _md_of(page):
    try:
        return page.evaluate(GET_MD) or ""
    except Exception:
        return ""


def _md_titles(md):
    """md 中所有 ## 标题(归一化)"""
    out = []
    for ln in md.split("\n"):
        m = re.match(r"^#{2,}\s+(.+)$", ln)
        if m:
            t = norm_t(m.group(1))
            if t:
                out.append(t)
    return out


def _wait_changed(page, prev_md, timeout=12.0, poll=0.6, stable_n=3):
    """等 markdown 变成与 prev_md 不同且稳定下来"""
    t0 = time.time()
    last, stable = "", 0
    while time.time() - t0 < timeout:
        time.sleep(poll)
        md = _md_of(page)
        if not md or md == prev_md:
            last, stable = "", 0
            continue
        if md == last:
            stable += 1
            if stable >= stable_n:
                return True
        else:
            stable, last = 0, md
    return False


def harvest_burst(page, screens, prev_md, duration=6.0, poll=0.25, stable_end=1.8,
                  fast=False):
    """⭐⭐ 连采: 阅读器分栏渲染(左栏画完 clear 再画右栏), hook 每次 clear 都重置
    markdown —— 只在翻屏后取一次快照会漏掉整栏正文(实测每屏只拿到右栏197字,
    截图里可见约420字)。改为翻屏后高频采样, 把每个中间态都收下来。
    重复渲染(重新排版)用"新 md 前60字是否已在已收正文里"去重。
    fast=True 时收紧采样窗(大章塞进10分钟前台上限)。"""
    if fast:
        duration, poll, stable_end = 5.0, 0.2, 1.4
    t0 = time.time()
    last = prev_md
    last_change = time.time()
    while time.time() - t0 < duration:
        md = _md_of(page)
        if md and md != last:
            tail = "".join(screens)[-3000:]
            if last and md.startswith(last) and len(md) > len(last):
                screens.append(md[len(last):])
                last, last_change = md, time.time()
            elif md[:60] and md[:60] in tail:
                last = md                      # 重复/回退渲染, 丢弃
            else:
                screens.append(md)
                last, last_change = md, time.time()
        if (time.time() - last_change > stable_end) and (time.time() - t0 > 1.5):
            break
        time.sleep(poll)
    return last


def export_chapter_v4(page, url_base, k, out_path, expect_title="",
                      toc_norms=frozenset(), wc=0, pace="normal",
                      max_back=90, max_fwd=240):
    pre_s = 1.3 if pace == "fast" else 2.2
    ne = norm_t(expect_title)
    url = url_base + k
    part_path = out_path + ".part"

    def finalize(screens):
        text = "\n".join(screens).strip()
        text = slice_chapter(text, expect_title, toc_norms) \
            if (expect_title and toc_norms) else text
        text = text.replace("<sup>", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        m = re.match(r"^#{2,}\s+(.+)$", text, re.M)
        first_t = norm_t(m.group(1)) if m else ""
        if expect_title and first_t != ne:
            text = "## %s\n\n%s" % (expect_title, text)
        return text

    try:
        page.bring_to_front()
    except Exception:
        pass
    try:   # ⭐ 单栏视口: 双 canvas 跨页会丢一半正文
        page.set_viewport_size(VIEWPORT)
    except Exception:
        pass
    # ---- 1) 单次 goto(不诱饵) ----
    landed = False
    for _a in range(3):
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            landed = True
            break
        except Exception:
            time.sleep(3)
    if not landed:
        return 0, False, "goto-fail"
    time.sleep(4.0)
    wait_render(page, timeout=45)
    try:
        page.bring_to_front()
    except Exception:
        pass

    prev_md = _md_of(page)

    def cur_chapter():
        try:
            return norm_t(page.evaluate(JS_CUR_CHAPTER) or "")
        except Exception:
            return ""

    # ---- 2) 回退定位到章首 ----
    #    落地在"服务器同步位置"(实测常在章末), 先回退到刚离开本章为止,
    #    再前进一屏回到本章第一屏。回退屏不渲染章标题, 用顶部栏章名判定。
    back, stalls, at_start = 0, 0, False
    if ne and (ne in _md_titles(prev_md)):
        at_start = True                     # 落地即章首(未读过的章)
    while not at_start and back < max_back:
        try:
            page.click(PREV_SEL, timeout=5000)
        except Exception:
            break                            # 已在全书最前
        back += 1
        time.sleep(pre_s)
        _wait_changed(page, prev_md, timeout=10, poll=0.5, stable_n=3)
        md = _md_of(page)
        if not md or md == prev_md:
            stalls += 1
            if stalls >= 3:
                break
            continue
        stalls = 0
        prev_md = md
        c = cur_chapter()
        if ne and c and c != ne:            # 已退回上一章 -> 前进一屏回到章首
            try:
                page.click(NEXT_SEL, timeout=5000)
                time.sleep(pre_s)
                back -= 1
            except Exception:
                pass
            break
        ts = _md_titles(md)
        if ne and ne in ts:                 # 回退屏偶尔也带本章标题 -> 到章首了
            break
        if DEBUG and back % 5 == 0:
            print("    [dbg] 回退%d屏 章名=%s" % (back, c[:14]), flush=True)

    # ---- 3) 正向采收 ----
    screens = []
    prev_md = ""
    stalls = 0
    end_reason = "unknown"

    def harvest():
        nonlocal prev_md
        md = _md_of(page)
        if not md or md == prev_md:
            return False
        tail = "".join(screens)[-3000:]
        if prev_md and md.startswith(prev_md) and len(md) > len(prev_md):
            screens.append(md[len(prev_md):])
        elif md[:60] and md[:60] in tail:
            prev_md = md
            return False
        else:
            screens.append(md)
        prev_md = md
        return True

    harvest()
    prev_md = harvest_burst(page, screens, prev_md, fast=(pace == "fast"))   # 首屏也要连采(分栏)
    for i in range(max_fwd):
        try:
            with open(part_path, "w", encoding="utf-8", newline="") as f:
                f.write(finalize(screens))
        except Exception:
            pass
        joined = "".join(screens)
        if toc_norms and find_heading_cut(joined, expect_title, toc_norms) is not None:
            end_reason = "next-heading"
            break
        try:
            st = page.evaluate(JS_FIND_PAGE)
        except Exception:
            end_reason = "page-error"
            break
        if st != "PAGE":
            end_reason = "btn:" + str(st)[:24]
            break
        try:
            page.click(NEXT_SEL, timeout=5000)
        except Exception:
            end_reason = "click-fail"
            break
        time.sleep(pre_s)
        before = sum(len(x) for x in screens)
        prev_md = harvest_burst(page, screens, prev_md, fast=(pace == "fast"))   # ⭐ 连采整屏(含分栏中间态)
        if sum(len(x) for x in screens) > before:
            stalls = 0
        else:
            stalls += 1
            if stalls >= 3:
                end_reason = "stall"
                break
        # ⭐ 顶部栏章名变了 = 已进入下一章(章界屏还带着本章尾巴, 多收两轮再停)
        c = cur_chapter()
        if DEBUG:
            print("    [dbg] 屏%d 章名=%s" % (i + 1, c[:20]), flush=True)
        if ne and c and c != ne:
            prev_md = harvest_burst(page, screens, prev_md, fast=(pace == "fast"))   # 章界屏带着本章尾巴
            end_reason = "chapter-change"
            break
        if DEBUG and (i + 1) % 5 == 0:
            print("    [dbg] 正向%d屏 累计%d字" %
                  (i + 1, sum(len(x) for x in screens)), flush=True)
    else:
        end_reason = "maxfwd"

    text = finalize(screens)
    if not text:
        if os.path.isfile(part_path):
            os.remove(part_path)
        return 0, False, "no-content"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    if os.path.isfile(part_path):
        os.remove(part_path)
    return len(text), True, end_reason + "/back%d" % back


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
    ap.add_argument("--fast", action="store_true",
                    help="长章专用: 翻屏节奏 1.0s/0.5s(默认 2.0s/1.0s 人工节奏)")
    ap.add_argument("--nofast", action="store_true",
                    help="强制 normal 节拍(关掉 auto-fast): 保证顶部栏章名判据有效, 章界不漏切")
    ap.add_argument("--force", action="store_true", help="重导已存在章节(修截断用)")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--maxpages", type=int, default=200)
    ap.add_argument("--v3", action="store_true", help="退回 v3 诱饵跳转路线(不推荐)")
    ap.add_argument("--chapters-json", default="", help="覆盖章节清单路径(库外暂存区用)")
    ap.add_argument("--out-dir", default="", help="覆盖输出目录(库外暂存区用)")
    args = ap.parse_args()
    global DEBUG
    DEBUG = args.debug
    global MP_GLOBAL
    MP_GLOBAL = args.maxpages

    cfg = BOOKS[args.book]
    chap_path = args.chapters_json or os.path.join(cfg["dir"], "_chapters.json")
    full = json.load(open(chap_path, encoding="utf-8"))
    title_by_uid = {str(c["chapterUid"]): c.get("title", "") for c in full}
    uid_order = [str(c["chapterUid"]) for c in full]
    # ⭐ 全书目录标题归一化集合: 只有命中它的 ## 行才算"下一章标题"
    toc_norms = frozenset(t for t in (norm_t(x) for x in title_by_uid.values()) if t)
    chapters = full
    if args.only:
        want = set(x.strip() for x in args.only.split(","))
        chapters = [c for c in full if str(c["chapterUid"]) in want]
    if args.range:
        a, b = (int(x) for x in args.range.split("-"))
        chapters = [c for c in chapters
                    if a <= uid_order.index(str(c["chapterUid"])) + 1 <= b]
    out_root = args.out_dir or os.path.join(cfg["dir"], "canvas")
    os.makedirs(out_root, exist_ok=True)

    root = "https://weread.qq.com/web/reader/" + cfg["vid"]
    url_base = root + ("?k=" if args.urlmode == "query" else "k")

    print("[start] book=%s 章节=%d url=%s... fast=%s force=%s"
          % (args.book, len(chapters), url_base[:60], args.fast, args.force), flush=True)

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
    t_start = time.time()
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
            for i, ch in enumerate(chapters, 1):
                uid = str(ch["chapterUid"])
                title = ch.get("title", "")
                wc = int(ch.get("wordCount", 0) or 0)
                if wc <= 5:
                    print("[skip] %03d %-30s wordCount=%d 空章" % (i, title[:30], wc),
                          flush=True)
                    continue
                # ⭐ 自动pace: >=15000字的长章用fast(塞进10分钟前台上限),
                #    但 fast 节拍下顶部栏章名判据失效 -> 章界漏切(溢出到下一章)。
                #    --nofast 时一律 normal(顶部栏判据可靠, 章界干净; 大章靠收紧采样窗塞进时限)。
                #    其余保持用户要求的人工慢速; --fast 可全局强制
                pace = "fast" if (not args.nofast and (args.fast or wc >= 15000)) else "normal"
                # ⭐ 时限检查放在开跑新章之前: 按本章字数估算耗时,
                #    长章放过去会被硬超时SIGTERM切死
                if args.minutes:
                    per_scr = 380.0
                    scr_s = 3.4 if pace == "fast" else 5.0
                    # v4 回退+正向 ≈ 2 倍屏数
                    est = (wc / per_scr) * (1.0 if args.v3 else 2.0) * scr_s + 30
                    if (time.time() - t_start) + est > args.minutes * 60:
                        print("[stop] 时限预算不足(本章约%.1f分钟), 干净退出 (进度已落盘, 重跑自动续)"
                              % (est / 60), flush=True)
                        break
                pos = uid_order.index(uid)
                # ⭐ 文件名序号用全文章节位置(pos+1), 不能用过滤后列表的 i
                fname = "%03d-%s.md" % (pos + 1, slug(title))
                out = os.path.join(out_root, fname)
                if (os.path.isfile(out) and os.path.getsize(out) > 30
                        and not args.force):
                    print("[skip] %s 已存在 %d字节" % (fname, os.path.getsize(out)), flush=True)
                    continue
                # 诱饵章: 目录里的上一章(把阅读器位置挪离目标章)
                decoy_uid = uid_order[pos - 1] if pos > 0 else (
                    uid_order[1] if len(uid_order) > 1 else "")
                if args.v3:
                    n, ok, reason = export_chapter(
                        ctx, shared, url_base, wr_hash(uid), out,
                        expect_title=title, toc_norms=toc_norms,
                        decoy_k=wr_hash(decoy_uid) if decoy_uid else "",
                        pace=pace)
                else:
                    n, ok, reason = export_chapter_v4(
                        shared, url_base, wr_hash(uid), out,
                        expect_title=title, toc_norms=toc_norms,
                        wc=wc, pace=pace)
                if ok:
                    total_chars += n
                    ok_n += 1
                    idx_map.append((os.path.basename(out), title, uid, n))
                    print("[%3d/%3d] %-30s %6d字 end=%-16s(累计%d)" %
                          (pos + 1, len(full), title[:30], n, reason, total_chars), flush=True)
                else:
                    print("[%3d/%3d] %-30s !! 无内容 (%s)" %
                          (pos + 1, len(full), title[:30], reason), flush=True)
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
