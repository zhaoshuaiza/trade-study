#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信读书中文书抓取器（Playwright 拦截 /web/book/chapter/e_N 分块流）

原理（已实测打通）：
  - 微信读书正文不在 DOM，渲染到 <canvas>，普通抓取拿不到文字。
  - 内容通过接口 /web/book/chapter/e_N 返回，body 结构为：
        前 32 字节 token + 第 33 字节 'P' + base64(章节 xhtml 字节流分块)
  - e_N 是「相对当前阅读位置的分块流」，非绝对章号；每次翻章产生一个新 e_N 响应。
  - 把每个 e_N 响应解码后按 </html> 切分，即得每章干净 XHTML。
  - TOC 跳转在会员顺序阅读下被锁（多数章节 disabled），但「下一章」真实点击可逐章放行。

用法：
  python _fetch_weread.py --book 2015 --cookie-file _cookie.txt
  python _fetch_weread.py --book 2002 --cookie-file _cookie.txt --max 3   # 先探测3章
  python _fetch_weread.py --book 2015 --cookie-file _cookie.txt           # 全本

特性：
  - 增量保存：已落盘的 .txt 内容 hash 去重，中断可续跑，不重复抓。
  - 每章落盘 0000.html / 0000.txt，并写 _meta.json 章节清单。
"""

import sys, os, re, base64, json, time, argparse
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))

BOOKS = {
    "2015": {
        "book_id": "3300129049",
        "reader": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623",
        "out": os.path.join(ROOT, "raw/distilled/steenbarger-2015-zh"),
    },
    "2002": {
        "book_id": "3300220786",
        "reader": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b",
        "out": os.path.join(ROOT, "raw/distilled/steenbarger-2002-zh"),
    },
}


def parse_cookie(s):
    """把浏览器复制的 Cookie 头字符串解析成 Playwright cookies。"""
    out = []
    for part in s.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        out.append({"name": k.strip(), "value": v.strip(),
                    "domain": ".qq.com", "path": "/"})
    return out


def decode_body(body):
    """body: bytes。返回解码后的 xhtml 字符串，或 None。"""
    if not body or len(body) <= 33:
        return None
    if body[32:33] != b"P":
        return None
    try:
        return base64.b64decode(body[33:]).decode("utf-8", "ignore")
    except Exception:
        return None


def xhtml_to_text(x):
    """从单章 xhtml 抽取标题与纯文本。"""
    m = re.search(r"<title>(.*?)</title>", x, re.S)
    title = m.group(1).strip() if m else ""
    x2 = re.sub(r"<style[\s\S]*?</style>", "", x)
    x2 = re.sub(r"<script[\s\S]*?</script>", "", x2)
    blocks = re.split(r"</p>|</div>|<br\s*/?>|</h\d>", x2)
    paras = []
    for b in blocks:
        t = re.sub(r"<[^>]+>", "", b)
        t = t.replace("&nbsp;", " ")
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


def save_chapter(out_dir, idx, title, xhtml, text):
    with open(os.path.join(out_dir, f"{idx:04d}.html"), "w", encoding="utf-8") as f:
        f.write(xhtml)
    with open(os.path.join(out_dir, f"{idx:04d}.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  [saved] ch{idx:04d} title={title!r} chars={len(text)}")


def write_meta(out_dir, chapters):
    with open(os.path.join(out_dir, "_meta.json"), "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=["2015", "2002"])
    ap.add_argument("--cookie-file", default=os.path.join(ROOT, "_cookie.txt"))
    ap.add_argument("--max", type=int, default=0, help="最多抓几章(0=全本)")
    ap.add_argument("--headless", action="store_true", default=True)
    args = ap.parse_args()

    cfg = BOOKS[args.book]
    out_dir = cfg["out"]
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isfile(args.cookie_file):
        print(f"[ERROR] cookie 文件不存在: {args.cookie_file}")
        sys.exit(2)
    with open(args.cookie_file, encoding="utf-8") as fh:
        cookie_str = fh.read().strip()
    cookies = parse_cookie(cookie_str)

    proxy = None
    env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if env_proxy:
        proxy = {"server": env_proxy}

    # 已落盘内容 hash，用于去重续跑
    saved = set()
    for f in os.listdir(out_dir):
        if re.match(r"\d+\.txt$", f):
            try:
                with open(os.path.join(out_dir, f), encoding="utf-8") as fh:
                    saved.add(hash(fh.read()))
            except Exception:
                pass

    chapters = []          # 本次与历史合并的章节清单
    captured_hashes = set(saved)
    new_count = 0

    def on_response(response):
        nonlocal new_count
        url = response.url
        last = url.rstrip("/").split("/")[-1]
        if "/web/book/chapter/" not in url or not last.startswith("e_"):
            return
        try:
            body = response.body()
        except Exception:
            return
        dec = decode_body(body)
        if not dec:
            return
        # 按 </html> 切分，每个片段是一章 xhtml
        parts = re.split(r"</html>", dec)
        for p in parts:
            p = p.strip()
            if not p or "<" not in p:
                continue
            xhtml = p if p.endswith("</html>") else p + "</html>"
            title, text = xhtml_to_text(xhtml)
            if not text or len(text) < 50:
                continue
            h = hash(text)
            if h in captured_hashes:
                continue
            captured_hashes.add(h)
            idx = next_index(out_dir)
            save_chapter(out_dir, idx, title, xhtml, text)
            chapters.append({"n": idx, "title": title, "chars": len(text)})
            new_count += 1

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=args.headless, proxy=proxy, args=["--no-sandbox"])
        ctx = browser.new_context()
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        page.on("response", on_response)

        print(f"[open] {cfg['reader']}")
        page.goto(cfg["reader"], wait_until="networkidle", timeout=60000)
        time.sleep(3)

        # 粗略登录态检查：页面是否提示登录
        body_text = page.evaluate("() => document.body.innerText") or ""
        if "登录" in body_text[:200] or "请先登录" in body_text:
            print("[WARN] 页面显示未登录，Cookie 可能已过期。请更新 _cookie.txt 后重试。")
            browser.close()
            sys.exit(3)

        turn = 0
        max_turn = 4000
        while True:
            if args.max and new_count >= args.max:
                print(f"[done] 已达 --max={args.max} 章上限")
                break
            before = new_count

            # 翻章策略：先点击阅读区中部聚焦，再 ArrowRight；随后尝试「下一章」按钮
            try:
                page.mouse.click(600, 400)
            except Exception:
                pass
            page.keyboard.press("ArrowRight")
            time.sleep(1.0)

            # 尝试点击「下一章」按钮（文本匹配）
            try:
                btn = page.query_selector("text=下一章")
                if btn:
                    btn.click()
            except Exception:
                pass
            time.sleep(2.0)

            if new_count == before:
                # 再尝试通用翻页按钮（类名含 next/page/turn）
                try:
                    for sel in [".readerFooterButton.right", ".app_reader .next",
                                "[class*=next]", "[class*=page]"]:
                        el = page.query_selector(sel)
                        if el:
                            el.click()
                            break
                except Exception:
                    pass
                time.sleep(2.0)

            if new_count == before:
                # 连续两次无新章：可能是到末尾，或翻章方式失效
                turn += 1
                if turn >= 2:
                    print("[stop] 连续无新章节，疑似到末尾或登录失效")
                    break
            else:
                turn = 0

            max_turn -= 1
            if max_turn <= 0:
                print("[stop] 达到最大翻页次数")
                break

        # 合并历史 _meta 后再写
        try:
            with open(os.path.join(out_dir, "_meta.json"), encoding="utf-8") as fh:
                old = json.load(fh)
        except Exception:
            old = []
        merged = {c["n"]: c for c in (old + chapters)}
        write_meta(out_dir, [merged[k] for k in sorted(merged)])
        print(f"[summary] 本书累计章节文件: {next_index(out_dir)} 个；本次新增: {new_count}")
        browser.close()


if __name__ == "__main__":
    main()
