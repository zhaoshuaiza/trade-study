#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
方案：复制 Edge profile（含完整 HttpOnly cookie）-> headless 加载 -> 复用真实登录态。
新版 Edge/Chrome 的 cookie 库位于 User Data\Default\Network\Cookies
"""
import os, shutil
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\admi\AppData\Local\Microsoft\Edge\User Data"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DST = os.path.join(ROOT, ".edge_profile")

os.makedirs(os.path.join(DST, "Default", "Network"), exist_ok=True)


def cp(src, dst, label):
    try:
        shutil.copy2(src, dst)
        print("copied:", label)
    except Exception as e:
        print("fail:", label, e)


cp(os.path.join(SRC, "Local State"), os.path.join(DST, "Local State"), "Local State")
cp(os.path.join(SRC, "Default", "Network", "Cookies"),
   os.path.join(DST, "Default", "Network", "Cookies"), "Default/Network/Cookies")
cp(os.path.join(SRC, "Default", "Network", "Cookies-journal"),
   os.path.join(DST, "Default", "Network", "Cookies-journal"), "Cookies-journal")
cp(os.path.join(SRC, "Default", "Preferences"),
   os.path.join(DST, "Default", "Preferences"), "Default/Preferences")
cp(os.path.join(SRC, "Default", "Network", "Network Persistent State"),
   os.path.join(DST, "Default", "Network", "Network Persistent State"),
   "Network Persistent State")

proxy = None
ep = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if ep:
    proxy = {"server": ep}

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=SRC,  # 直接用原始 profile：App-Bound 加密绑定原路径，复制会解不开
        headless=False,  # 新版 Edge 不支持旧 --headless，改由 args 指定 --headless=new
        executable_path=EDGE,
        proxy=proxy,
        args=["--headless=new", "--no-sandbox", "--disable-gpu",
              "--disable-dev-shm-usage"],
    )
    cs = ctx.cookies()
    wr = {c["name"]: c["value"] for c in cs if "weread" in (c.get("domain") or "")}
    print("weread cookie keys:", list(wr.keys()))
    for k in ("wr_vid", "wr_skey", "wr_rt"):
        v = wr.get(k)
        print(f"  {k}: {'YES len=' + str(len(v)) if v else 'MISSING'}")
    page = ctx.new_page()
    try:
        r = page.request.get("https://weread.qq.com/web/shelf/sync")
        print("shelf/sync:", r.text()[:200])
    except Exception as e:
        print("shelf error:", repr(e))
    ctx.close()
