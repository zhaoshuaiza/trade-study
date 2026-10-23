#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""在受控 Edge 中打开微信读书登录页，截取二维码图片，供用户扫码登录。"""
import os, sys, time

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
QR_PATH = os.path.join(ROOT, "_login_qr.png")
FULL_PATH = os.path.join(ROOT, "_login_full.png")

CHECK_MODE = "--check" in sys.argv


def logged_in(page):
    """用页面 UI 特征判断是否已登录（头像/我的 按钮）。"""
    try:
        return page.evaluate("""() => {
            const t = document.body.innerText || '';
            return !t.includes('登录') || !!document.querySelector('.avatar img, .wr_avatar, [class*=avatar] img');
        }""")
    except Exception:
        return False


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.set_viewport_size({"width": 1380, "height": 940})
        except Exception:
            pass  # 有头模式不支持 metrics override，忽略

        if CHECK_MODE:
            page.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=40000)
            time.sleep(5)
            print("URL:", page.url)
            print("LOGGED_IN:", logged_in(page))
            b.close()
            return

        page.goto("https://weread.qq.com/", wait_until="domcontentloaded", timeout=40000)
        time.sleep(5)
        print("URL:", page.url)

        # 点右上角"登录"
        clicked = False
        for sel in ["text=登录", "button:has-text('登录')", "a:has-text('登录')", ".login_button", "[class*=login]"]:
            try:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=1500):
                    loc.click()
                    clicked = True
                    print("CLICKED:", sel)
                    break
            except Exception:
                pass
        if not clicked:
            print("NO LOGIN BUTTON FOUND - maybe already logged in; LOGGED_IN:", logged_in(page))
        time.sleep(6)

        # 找二维码
        sel = None
        for cand in ["img[class*=qrcode]", "canvas[class*=qrcode]", "img[src*='qrcode']",
                     ".login_qrcode img", ".qrcode", "[class*=qrcode] img", "[class*=qrcode] canvas"]:
            try:
                loc = page.locator(cand).first
                if loc.is_visible(timeout=1200):
                    sel = cand
                    break
            except Exception:
                pass
        try:
            page.screenshot(path=FULL_PATH)
            print("FULL SAVED:", FULL_PATH)
        except Exception as e:
            print("FULL SHOT FAIL", e)
        if sel:
            try:
                page.locator(sel).first.screenshot(path=QR_PATH)
                print("QR SAVED(element):", sel)
            except Exception as e:
                print("QR ELEMENT SHOT FAIL", e)
                sel = None
        if not sel:
            page.screenshot(path=QR_PATH, clip={"x": 430, "y": 140, "width": 520, "height": 660})
            print("QR SAVED(region fallback)")
        print("LOGGED_IN:", logged_in(page))
        b.close()


if __name__ == "__main__":
    main()
