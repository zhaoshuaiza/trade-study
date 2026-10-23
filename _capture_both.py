#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""恢复后顺序抓取两本书(2015 全本慢抓 + 2002 全本首抓)。"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = "C:/Users/admi/.workbuddy/binaries/python/versions/3.13.12/python3"
SITE = "C:/Users/admi/.workbuddy/binaries/python/envs/default/Lib/site-packages"
# 子进程需要能 import playwright
ENV = os.environ.copy()
ENV["PYTHONPATH"] = SITE + (";" + ENV["PYTHONPATH"] if ENV.get("PYTHONPATH") else "")


def run(book):
    print("\n##### 开始抓取 %s #####" % book, flush=True)
    cmd = [PY, "-u", os.path.join(ROOT, "_capture_v3.py"),
           "--book", book, "--pause", "2.8", "--idle", "150",
           "--maxpress", "2500", "--first", "backward"]
    log = open(os.path.join(ROOT, "_fullpass_%s.log" % book), "w", encoding="utf-8")
    r = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=ENV)
    print("##### %s 结束, exit=%s #####" % (book, r.returncode), flush=True)
    return r.returncode


def main():
    run("2015")
    run("2002")
    print("\n===== 两书抓取完成 =====", flush=True)


if __name__ == "__main__":
    main()
