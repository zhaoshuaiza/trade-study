#!/usr/bin/env python3
# 登录态下抓取《从躺椅上操作：交易心理学》章节清单 -> _chapters.json
import json, os, time, sys
from playwright.sync_api import sync_playwright

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PROFILE = "E:/_edge_fresh"
PORT = 9222
VID = "72a327c0811e260b2g017333"
OUT = "E:/Work Buddy/交易学习/raw/distilled/steenbarger-2002-tradepsych-zh/_chapters.json"
ROOT = "E:/Work Buddy/交易学习"

def main():
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=PROFILE, headless=False, executable_path=EDGE,
            args=[f"--remote-debugging-port={PORT}", "--no-first-run",
                  "--no-default-browser-check", "--window-size=900,1000"],
        )
        pg = ctx.new_page()
        pg.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(4000)
        body = pg.evaluate("()=>document.body.innerText") or ""
        print("LOGIN?", ("我的书架" in body) or ("登录" not in body), "| 登录Btn?", "登录" in body)
        if "登录" in body and "我的书架" not in body:
            print("NOT_LOGGED_IN — 需要扫码"); ctx.close(); sys.exit(2)

        # 尝试 A: chapterInfos API (带 cookie)
        apis = [
            f"https://weread.qq.com/web/book/chapterInfos?bookId={VID}",
            f"https://weread.qq.com/web/book/getChapterInfos?bookId={VID}",
        ]
        chapters = None
        for ep in apis:
            try:
                txt = pg.evaluate("(url)=>fetch(url,{credentials:'include'}).then(r=>r.text()).catch(e=>'ERR:'+e)", ep)
                print("API", ep.split('/')[-1], "->", repr(txt[:160]))
                try:
                    d = json.loads(txt)
                    # 常见结构 data / chapterInfos
                    ch = d.get("data") or d.get("chapterInfos") or (d if isinstance(d, list) else None)
                    if isinstance(ch, list) and ch:
                        chapters = ch
                        print("  GOT", len(ch), "chapters via API")
                        break
                except Exception:
                    pass
            except Exception as e:
                print("API_ERR", e)

        # 尝试 B: reader 目录面板
        if not chapters:
            pg.goto(f"https://weread.qq.com/web/reader/{VID}", wait_until="domcontentloaded", timeout=30000)
            pg.wait_for_timeout(5000)
            for sel in ["button:has-text('目录')", "[class*=catalog]"]:
                try:
                    el = pg.query_selector(sel)
                    if el:
                        try: el.click(timeout=2000)
                        except Exception: pg.evaluate("(e)=>e.click()", el)
                        print("clicked", sel); break
                except Exception: pass
            pg.wait_for_timeout(3000)
            items = pg.evaluate("""() => {
                const links=[...document.querySelectorAll('a[href*=chapterUid]')];
                const out=[];
                for(const a of links){
                    const m=a.getAttribute('href').match(/chapterUid=(\\d+)/);
                    out.push({uid:m?m[1]:null, t:(a.innerText||'').trim()});
                }
                // 也抓目录列表项
                const lis=[...document.querySelectorAll('[class*=chapterItem],[class*=catalogItem],li')];
                return {links:out.slice(0,8), liCount:lis.length,
                        liSample: lis.slice(0,8).map(l=>({t:(l.innerText||'').trim().slice(0,30), uid:(l.getAttribute('data-chapter-uid')||'')}))};
            }""")
            print("CATALOG:", json.dumps(items, ensure_ascii=False)[:600])
            if items.get("links"):
                chapters = []
                for ln in items["links"]:
                    if ln["uid"] and ln["t"]:
                        chapters.append({"chapterUid": int(ln["uid"]), "title": ln["t"], "chapterIdx": 0, "wordCount": 0, "level": 1})
                print("  GOT", len(chapters), "from catalog links")

        if chapters:
            # 规整为导出脚本需要的字段
            norm = []
            for i, c in enumerate(chapters, 1):
                norm.append({
                    "chapterUid": c.get("chapterUid") or c.get("chapterIdx") or i,
                    "chapterIdx": c.get("chapterIdx", i),
                    "title": c.get("title", "") or c.get("chapterTitle", ""),
                    "wordCount": c.get("wordCount", 0) or 0,
                    "level": c.get("level", 1),
                    "isMPChapter": c.get("isMPChapter", 0),
                })
            os.makedirs(os.path.dirname(OUT), exist_ok=True)
            json.dump(norm, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("SAVED", OUT, len(norm), "chapters")
            print(json.dumps(norm[:3], ensure_ascii=False))
        else:
            print("NO_CHAPTERS_FOUND")
        ctx.close()

if __name__ == "__main__":
    main()
