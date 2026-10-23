#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""冷却自愈: 每 N 分钟用 1 个轻量请求探测正文接口是否恢复; 恢复即自动启动逐屏抓取。

python _cdp_wait_resume.py --book 2015 --maxwait 90 [--every 5]
"""
import os, re, sys, time, json, argparse, subprocess

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOKS = {
    "2015": {"reader": "https://weread.qq.com/web/reader/33d32010813ab98e8g019623"},
    "2002": {"reader": "https://weread.qq.com/web/reader/5ea329c0813abbcbeg01667b"},
}
PY = "C:/Users/admi/.workbuddy/binaries/python/versions/3.13.12/python3"
SITE = "C:/Users/admi/.workbuddy/binaries/python/envs/default/Lib/site-packages"
ENV = os.environ.copy()
ENV["PYTHONPATH"] = SITE + (";" + ENV["PYTHONPATH"] if ENV.get("PYTHONPATH") else "")

PROBE = """async (p0) => {
  try {
    const r = await fetch('/web/book/chapter/e_0', {method:'POST', credentials:'include',
      headers:{'Content-Type':'application/json;charset=UTF-8'},
      body: JSON.stringify({...p0, ct: Math.floor(Date.now()/1000)})});
    const t = await r.text();
    return [r.status, t.length];
  } catch (e) { return ['ERR', String(e).slice(0,80)]; }
}"""
P0 = {"b": "33d32010813ab98e8g019623", "c": "861322a025a8613985ec87a", "r": 9865881, "st": 0,
      "ps": "326321207aaf520cg0171a3", "pc": "e5932ec07aaf520cg018303", "sc": 0, "s": "5290312e"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, choices=list(BOOKS))
    ap.add_argument("--maxwait", type=float, default=90, help="最长等待分钟数")
    ap.add_argument("--every", type=float, default=5, help="探测间隔分钟")
    args = ap.parse_args()

    t0 = time.time()
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0]
        try:
            page.goto(BOOKS[args.book]["reader"], wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("[nav]", str(e)[:60])
        time.sleep(10)

        round_no = 0
        while (time.time() - t0) < args.maxwait * 60:
            round_no += 1
            try:
                st, ln = page.evaluate(PROBE, P0)
            except Exception as e:
                st, ln = "ERR", str(e)[:60]
            mins = (time.time() - t0) / 60
            print("[%5.1fmin] 第%d次探测 -> status=%s len=%s" % (mins, round_no, st, ln), flush=True)
            if st == 200 and isinstance(ln, int) and ln > 500:
                print("[恢复] 正文接口已恢复(len=%s),启动两书完整慢速抓取" % ln, flush=True)
                log = open(os.path.join(ROOT, "_resume_%s.log" % args.book), "w", encoding="utf-8")
                # 顺序抓取 2015(补抓/复核) + 2002(首抓), 慢速双程覆盖全书
                cmd = [PY, "-u", os.path.join(ROOT, "_capture_both.py")]
                try:
                    b.close()  # 先释放本进程的浏览器连接, 交给抓取进程
                except Exception:
                    pass
                r = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=ENV)
                print("[抓取进程结束] exit=%s" % r.returncode, flush=True)
                return
            time.sleep(args.every * 60)
        print("[timeout] %g 分钟内未恢复,停止等待" % args.maxwait, flush=True)


if __name__ == "__main__":
    main()
