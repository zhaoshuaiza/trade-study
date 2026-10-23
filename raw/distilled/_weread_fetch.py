# -*- coding: utf-8 -*-
"""
微信读书(weread) 单本书正文抓取脚手架。
用法（拿到 cookie 后）:
  python _weread_fetch.py "<cookie字符串>" <bookId> [输出目录]

说明:
- 先用 book/info 核验书名作者(防抓错书)
- 再拉 chapterInfos 拿章节清单
- 逐章拉 content(返回 base64 混淆正文), base64 解码后落盘 raw 供人工/二次解码检查
- 解码逻辑在拿到真实数据后于 _decode() 内确定, 此处先留 base64 直解
"""
import sys, os, base64, json, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def http_get(url, cookie):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Referer", "https://weread.qq.com/")
    req.add_header("Cookie", cookie)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

def http_get_json(url, cookie):
    return json.loads(http_get(url, cookie))

def fetch_book_info(book_id, cookie):
    url = "https://weread.qq.com/web/book/info?bookId=" + book_id
    return http_get_json(url, cookie)

def fetch_chapter_infos(book_id, cookie):
    url = "https://weread.qq.com/web/book/chapterInfos?bookIds=" + book_id
    return http_get_json(url, cookie)

def fetch_chapter_content(book_id, chapter_uid, cookie):
    url = "https://weread.qq.com/web/book/content?bookId=%s&chapterUid=%s" % (book_id, chapter_uid)
    return http_get_json(url, cookie)

def decode_content(b64):
    """占位解码: 先 base64 直解, 真实 de-obfuscate 待观测后补全。"""
    try:
        raw = base64.b64decode(b64).decode("utf-8", "ignore")
    except Exception:
        raw = ""
    return raw

def main():
    # cookie 优先从环境变量 WR_COOKIE 读取(避免命令行暴露), 否则取 argv[1]
    env_cookie = os.environ.get("WR_COOKIE")
    if env_cookie:
        cookie = env_cookie
        book_id = sys.argv[1]
        outdir = sys.argv[2] if len(sys.argv) > 2 else ("_weread_tmp/" + book_id)
    else:
        if len(sys.argv) < 3:
            print("usage: WR_COOKIE='...' python _weread_fetch.py <bookId> [outdir]  (或 _weread_fetch.py <cookie> <bookId> [outdir])")
            sys.exit(1)
        cookie = sys.argv[1]
        book_id = sys.argv[2]
        outdir = sys.argv[3] if len(sys.argv) > 3 else ("_weread_tmp/" + book_id)
    os.makedirs(outdir, exist_ok=True)

    print("=== [1/3] 书籍身份核验 ===")
    info = fetch_book_info(book_id, cookie)
    print(json.dumps(info, ensure_ascii=False, indent=2)[:1500])

    print("\n=== [2/3] 章节清单 ===")
    chap = fetch_chapter_infos(book_id, cookie)
    chapters = chap.get("data", [{}])[0].get("chapters", []) if "data" in chap else chap.get("chapters", [])
    print("章节数:", len(chapters))
    for c in chapters[:60]:
        print("  uid=%s lvl=%s | %s" % (c.get("chapterUid"), c.get("level"), c.get("title")))

    print("\n=== [3/3] 逐章拉取(原始base64解码落盘) ===")
    meta = []
    for i, c in enumerate(chapters):
        uid = c.get("chapterUid")
        title = c.get("title", "")
        try:
            content = fetch_chapter_content(book_id, uid, cookie)
            b64 = content.get("data", {}).get("content", "")
            text = decode_content(b64)
        except Exception as e:
            text = ""
            print("  ! 章 %s 失败: %s" % (uid, e))
        fname = os.path.join(outdir, "ch_%05d_%s.txt" % (i, uid))
        with open(fname, "w", encoding="utf-8") as f:
            f.write("【%s】\n%s" % (title, text))
        meta.append({"idx": i, "uid": uid, "title": title, "len": len(text), "file": fname})
        # 第一章打印前 600 字符, 供观测解码模式
        if i == 0:
            print("--- 第1章原始解码样本(前600字) ---")
            print(text[:600])
        print("  [%d/%d] uid=%s | %s | %d 字" % (i+1, len(chapters), uid, title, len(text)))

    with open(os.path.join(outdir, "chapters_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("\n完成. 输出目录:", outdir)

if __name__ == "__main__":
    main()
