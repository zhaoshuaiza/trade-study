# -*- coding: utf-8 -*-
"""综合探针：书架列表 + readInfo 全貌 + outline 三个变体 + 书内搜索。请求量刻意保持很小。"""
import os, time, json, io, re
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
BK = "3300129049"

JS = """async (bk) => {
  const out = {};
  const post = async (k, path, body) => {
    try {
      const r = await fetch(path, {method:'POST', credentials:'include',
        headers:{'Content-Type':'application/json;charset=UTF-8'}, body: JSON.stringify(body||{})});
      const t = await r.text(); out[k] = [r.status, t.length, t.slice(0, 600)];
    } catch(e) { out[k] = ['ERR', 0, String(e).slice(0,80)]; }
  };
  const get = async (k, path) => {
    try {
      const r = await fetch(path, {credentials:'include'});
      const t = await r.text(); out[k] = [r.status, t.length, t.slice(0, 600)];
    } catch(e) { out[k] = ['ERR', 0, String(e).slice(0,80)]; }
  };
  await get('shelf', '/web/shelf');
  await post('shelf_bookIds', '/web/shelf/bookIds', {});
  await post('readInfo_full', '/web/book/readInfo', {bookId: bk});
  await post('outlinePublic', '/web/book/outlinePublic', {bookId: bk});
  await post('outline_inner', '/web/book/outline/inner', {bookId: bk, chapterUids: [8, 9]});
  await post('briefOutline', '/web/book/briefOutline', {bookId: bk});
  await post('search_v2', '/web/book/search_v2', {bookId: bk, chapterUid: 8, posBegin: 0, posEnd: 0,
                                                  keyword: '埃米尔', mode: 'scrollDown', count: 5});
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
            st, ln, snip = v
            print("== %-16s %-4s len=%-7s" % (k, st, ln))
            print("   ", re.sub(r"\s+", " ", snip)[:520])

main()
