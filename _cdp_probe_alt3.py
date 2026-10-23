# -*- coding: utf-8 -*-
"""探针2：书内搜索（GET/POST 两种）+ 热门划线全文 + 单章划线结构。"""
import os, time, json, io, re
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
BK = "3300129049"

JS = """async (bk) => {
  const out = {};
  const get = async (k, path) => {
    try { const r = await fetch(path, {credentials:'include'}); const t = await r.text();
          out[k] = [r.status, t.length, t]; } catch(e) { out[k] = ['ERR', 0, String(e).slice(0,80)]; }
  };
  const post = async (k, path, body) => {
    try { const r = await fetch(path, {method:'POST', credentials:'include',
          headers:{'Content-Type':'application/json;charset=UTF-8'}, body: JSON.stringify(body||{})});
          const t = await r.text(); out[k] = [r.status, t.length, t]; }
    catch(e) { out[k] = ['ERR', 0, String(e).slice(0,80)]; }
  };
  await get('search_get', '/web/book/search?bookId=' + bk + '&keyword=' + encodeURIComponent('埃米尔'));
  await post('search_post', '/web/book/search', {bookId: bk, keyword: '埃米尔'});
  await get('bestbookmarks', '/web/book/bestbookmarks?bookId=' + bk);
  await get('underlines_89', '/web/book/underlines?bookId=' + bk + '&chapterUid=89');
  return out;
}"""

def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]; page = ctx.pages[0]; page.bring_to_front()
        try: page.goto(READER, wait_until="domcontentloaded", timeout=60000)
        except Exception as e: print("nav", str(e)[:60])
        time.sleep(7)
        res = page.evaluate(JS, BK)
        for k, v in res.items():
            st, ln, txt = v
            print("===== %s  status=%s len=%s" % (k, st, ln))
            if k in ("bestbookmarks", "underlines_89", "search_get", "search_post"):
                with open("_probe_%s.json" % k, "w", encoding="utf-8") as f:
                    f.write(txt)
                try:
                    d = json.loads(txt)
                    if k == "bestbookmarks":
                        chs = d.get("bestBookMarks", {}).get("chapters", [])
                        print("  chapters:", len(chs), "totalCount:", d.get("bestBookMarks", {}).get("totalCount"))
                        for c in chs[:3]:
                            print("   chapterUid", c.get("chapterUid"), "bookMarks", len(c.get("bookMarks", [])))
                            for bm in c.get("bookMarks", [])[:2]:
                                print("     ", json.dumps(bm, ensure_ascii=False)[:200])
                    elif k == "underlines_89":
                        ul = d.get("underlines", [])
                        print("  underlines:", len(ul))
                        for u in ul[:3]:
                            print("   ", json.dumps(u, ensure_ascii=False)[:220])
                    else:
                        print("  keys:", list(d)[:10])
                        print("  ", json.dumps(d, ensure_ascii=False)[:600])
                except Exception as e:
                    print("  [parse fail]", str(e)[:60], txt[:200])
            else:
                print("  ", re.sub(r"\s+", " ", txt)[:300])

main()
