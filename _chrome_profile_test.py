#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
方案：复制 Chrome profile -> headless 加载 -> 复用完整登录 cookie。
目的：绕开「HttpOnly 复制不到」与「GUI 进程在我会话里活不了」两个坑。
"""
import os, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\admi\AppData\Local\Google\Chrome\User Data"
CHROME = r"C:\Users\admi\AppData\Local\Google\Chrome\Application\chrome.exe"
DST = os.path.join(ROOT, ".chrome_profile")


def copy_profile():
    os.makedirs(os.path.join(DST, "Default"), exist_ok=True)
    copied = []
    # Local State 含 cookie 解密密钥，必须复制
    s = os.path.join(SRC, "Local State")
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(DST, "Local State"))
        copied.append("Local State")
    for f in ["Cookies", "Preferences"]:
        s = os.path.join(SRC, "Default", f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(DST, "Default", f))
            copied.append("Default/" + f)
    for ext in ["-journal", "-wal", "-shm"]:
        s = os.path.join(SRC, "Default", "Cookies" + ext)
        if os.path.exists(s):
            try:
                shutil.copy2(s, os.path.join(DST, "Default", "Cookies" + ext))
                copied.append("Cookies" + ext)
            except Exception as e:
                print("warn copy", ext, e)
    print("copied files:", copied)


copy_profile()

proxy = None
env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if env_proxy:
    proxy = {"server": env_proxy}

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=DST,
        headless=True,
        executable_path=CHROME,
        proxy=proxy,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
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
