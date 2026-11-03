#!/usr/bin/env python3
# 登录态下从 bookDetail 内嵌 __INITIAL_STATE__ 提取 chapterInfos
# 关键: 拦截图片/字体等大资源, 页面秒级就绪; wait_until=commit + 轮询状态
import json, os, sys
from playwright.sync_api import sync_playwright

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PROFILE = "E:/_edge_fresh"
PORT = 9222
VID = "72a327c0811e260b2g017333"
OUT = "E:/Work Buddy/交易学习/raw/distilled/steenbarger-2002-tradepsych-zh/_chapters.json"

def extract_state(pg):
    return pg.evaluate("""() => {
        const html = document.documentElement.outerHTML;
        const idx = html.indexOf('window.__INITIAL_STATE__');
        if (idx < 0) return {err:'no INITIAL_STATE'};
        const start = html.indexOf('=', idx) + 1;
        const end = html.indexOf('</script>', idx);
        let blob = html.slice(start, end).replace(/;\\s*$/, '').trim();
        try {
            const data = JSON.parse(blob);
            const ch = (data.reader && data.reader.chapterInfos) || data.chapterInfos;
            if (!ch) return {found:false, keys: Object.keys(data).slice(0,20)};
            return {found:true, count: ch.length, ch: ch};
        } catch(e) { return {parseErr: e.toString(), head: blob.slice(0,100)}; }
    }""")

def main():
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=PROFILE, headless=False, executable_path=EDGE,
            args=[f"--remote-debugging-port={PORT}", "--no-first-run",
                  "--no-default-browser-check", "--window-size=900,1000",
                  "--disable-dev-shm-usage", "--disable-gpu",
                  "--disable-extensions", "--no-zygote"],
        )
        pg = ctx.new_page()
        pg.goto(f"https://weread.qq.com/web/bookDetail/{VID}", wait_until="commit", timeout=40000)
        # 轮询状态
        result = None
        for _ in range(30):
            try:
                result = extract_state(pg)
                if result.get("found") or result.get("err") or result.get("parseErr"):
                    break
            except Exception as e:
                result = {"evalErr": str(e)}
            pg.wait_for_timeout(1000)
        print("STATE:", json.dumps(result, ensure_ascii=False)[:400])
        ch = (result.get("ch") if isinstance(result, dict) else None)
        if not ch:
            # 回退: 进 reader 读状态
            print("retry via reader ...")
            try:
                pg.goto(f"https://weread.qq.com/web/reader/{VID}", wait_until="commit", timeout=40000)
                for _ in range(30):
                    r2 = extract_state(pg)
                    if r2.get("found"): ch = r2.get("ch"); break
                    pg.wait_for_timeout(1000)
                print("READER_STATE:", json.dumps(r2, ensure_ascii=False)[:300])
            except Exception as e:
                print("reader err", e)
        if ch:
            norm = []
            for i, c in enumerate(ch, 1):
                norm.append({
                    "chapterUid": c.get("chapterUid", i),
                    "chapterIdx": c.get("chapterIdx", i),
                    "title": c.get("title", "") or c.get("chapterTitle", ""),
                    "wordCount": c.get("wordCount", 0) or 0,
                    "level": c.get("level", 1),
                    "isMPChapter": c.get("isMPChapter", 0),
                })
            json.dump(norm, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("SAVED", OUT, len(norm), "chapters")
            print(json.dumps(norm[:4], ensure_ascii=False))
        else:
            print("NO_CHAPTERS")
        ctx.close()

if __name__ == "__main__":
    main()
