# -*- coding: utf-8 -*-
"""批量抽取零OCR书的全文文本。
源: E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）/
输出: raw/distilled/{书名}-全文.txt + raw/books/_batch_extract.csv
"""
import io, os, csv, re, sys
import fitz  # pymupdf

SRC = "E:/Work Buddy/电子书/电子书资料每日更新（公众号私信 01 获取）"
OUT_DIR = "E:/Work Buddy/交易学习/raw/distilled"
SURVEY = "E:/Work Buddy/交易学习/raw/books/_survey_newbatch.csv"
CSV_OUT = "E:/Work Buddy/交易学习/raw/books/_batch_extract.csv"

# 已深度蒸馏过的，跳过
SKIP = {"032走出幻觉 走向成熟从学生股民到系统交易专家.pdf"}


def safe_name(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def main():
    with io.open(SURVEY, encoding="utf-8-sig") as fp:
        rows = list(csv.DictReader(fp))
    zero = [r for r in rows if r["verdict"] == "零OCR"]
    print(f"共 {len(zero)} 本零OCR待抽取")

    results = []
    for r in zero:
        fn = r["file"]
        if fn in SKIP:
            print(f"  跳过(已蒸馏): {fn[:40]}")
            continue
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            print(f"  文件缺失: {fn}")
            results.append({**r, "status": "缺失", "words": 0, "out": ""})
            continue
        book = r["book"]
        out_name = safe_name(book) + "-全文.txt"
        out_path = os.path.join(OUT_DIR, out_name)
        # 已抽过的跳过
        if os.path.exists(out_path):
            sz = os.path.getsize(out_path)
            print(f"  已存在({sz//1024}KB): {book[:40]}")
            results.append({**r, "status": "已存在", "words": sz, "out": out_name})
            continue
        try:
            doc = fitz.open(path)
            npages = doc.page_count
            parts = []
            for i in range(npages):
                t = doc[i].get_text()
                parts.append(f"\n=== 第{i+1}页 ===\n{t}")
            doc.close()
            text = "".join(parts)
            with io.open(out_path, "w", encoding="utf-8") as fp:
                fp.write(text)
            words = len(text)
            print(f"  ✅ {book[:40]:42s} p{npages:>4} {words//1024}KB")
            results.append({**r, "status": "OK", "words": words, "out": out_name, "pages": npages})
        except Exception as e:
            print(f"  ❌ {book[:40]} 失败: {e}")
            results.append({**r, "status": f"失败:{e}", "words": 0, "out": ""})

    # 写CSV
    fields = list(results[0].keys())
    with io.open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    ok = sum(1 for r in results if r["status"] in ("OK", "已存在"))
    print(f"\n完成: {ok}/{len(zero)} -> {CSV_OUT}")


if __name__ == "__main__":
    main()
