#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""列出所有 CDP target,确认阅读器到底在哪个 page/target。"""
import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 列出全部 context / page
        for ci, ctx in enumerate(b.contexts):
            print("=== context %d ===" % ci)
            for pi, pg in enumerate(ctx.pages):
                try:
                    u = pg.url
                    t = pg.title()
                except Exception as e:
                    u = "(err)"; t = str(e)[:40]
                print("  page[%d] url=%s title=%s" % (pi, u, t))
        # 直接问 CDP targets
        try:
            cdp0 = b.contexts[0].new_cdp_session(b.contexts[0].pages[0])
            targets = cdp0.send("Target.getTargets")
            print("=== CDP targets ===")
            for tg in targets.get("targetInfos", []):
                print("  ", tg.get("type"), tg.get("url")[:80])
        except Exception as e:
            print("getTargets fail", str(e)[:60])
        b.close()


if __name__ == "__main__":
    main()
