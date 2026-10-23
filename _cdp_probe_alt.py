# -*- coding: utf-8 -*-
"""停供期诊断：穷尽其他可能拿到正文/内容的接口路径（请求量极小）"""
import os, sys, json, io, re, time
os.environ["NO_PROXY"] = "127.0.0.1,localhost"; os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

READER2015 = "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
P0 = {"b":"33d32010813ab98e8g019623","c":"861322a025a8613985ec87a","r":9865881,"st":0,
      "ct":1792619654,"ps":"326321207aaf520cg0171a3","pc":"e5932ec07aaf520cg018303","sc":0,"s":"5290312e"}

JS = """
async (args) => {
  const out = [];
  const post = async (name, path, body) => {
    try {
      const r = await fetch(path, {method:'POST', credentials:'include',
        headers:{'Content-Type':'application/json;charset=UTF-8'}, body: JSON.stringify(body)});
      const t = await r.text();
      out.push([name, r.status, t.length, t.slice(0, 120)]);
    } catch(e) { out.push([name, 'ERR', 0, String(e).slice(0,80)]); }
  };
  const get = async (name, path) => {
    try {
      const r = await fetch(path, {credentials:'include'});
      const t = await r.text();
      out.push([name, r.status, t.length, t.slice(0, 120)]);
    } catch(e) { out.push([name, 'ERR', 0, String(e).slice(0,80)]); }
  };
  // 1) chapter 各分片
  for (const i of [0,1,2,3]) await post('chapter_e_'+i, '/web/book/chapter/e_'+i, args.p0);
  // 2) 换一个 chapterUid 再试
  const p1 = Object.assign({}, args.p0, {c: args.altc});
  await post('chapter_altc', '/web/book/chapter/e_0', p1);
  // 3) outline 单章（之前 13 章返回空的）
  await post('outline_single', '/web/book/outline', {bookId:'3300129049', chapterUids:[args.missuid]});
  // 4) 书签/划线/热门划线（可能带上下文文本）
  await get('bookmarklist', '/web/book/bookmarklist?bookId=3300129049&syncKey=0');
  await get('bestbookmarks', '/web/book/bestbookmarks?bookId=3300129049');
  await get('underlines', '/web/book/underlines?bookId=3300129049&chapterUid='+args.missuid);
  // 5) 其他可能承载正文的
  await get('readInfo', '/web/book/readInfo?bookId=3300129049');
  await post('chapterInfos', '/web/book/chapterInfos', {bookIds:['3300129049']});
  return out;
}
"""

def main():
    chs = json.load(io.open("raw/distilled/steenbarger-2015-zh/_chapters.json", encoding="utf-8"))
    alt = next((c["chapterUidHash"] for c in chs if c.get("chapterUid",0) in (1,2,3) and c.get("chapterUidHash")), None)
    miss = next((c["chapterUid"] for c in chs if c.get("chapterUid") == 89), 89)
    print("alt chapterUidHash:", alt, "| miss uid:", miss)
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]; page = ctx.pages[0]; page.bring_to_front()
        try: page.goto(READER2015, wait_until="domcontentloaded", timeout=60000)
        except Exception as e: print("nav", str(e)[:60])
        time.sleep(8)
        res = page.evaluate(JS, {"p0": P0, "altc": alt, "missuid": miss})
        for name, st, ln, snip in res:
            print("%-16s %-4s len=%-7s %s" % (name, st, ln, re.sub(r"\s+"," ", snip)[:100]))

main()
