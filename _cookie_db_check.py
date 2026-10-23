#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""只读打开 Edge cookie 数据库，确认 weread cookie 是否存在（不解密，只看域名和名字）"""
import sqlite3

P = r"C:\Users\admi\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"
con = sqlite3.connect("file:" + P + "?mode=ro", uri=True)
total = con.execute("select count(*) from cookies").fetchone()[0]
print("total cookies in DB:", total)
rows = con.execute(
    "select host_key, name, length(encrypted_value) from cookies where host_key like '%weread%'"
).fetchall()
print("weread rows:", len(rows))
for h, n, ln in rows:
    print(f"  {h}  {n}  enc_len={ln}")
print("--- top hosts ---")
for h, c in con.execute(
        "select host_key, count(*) c from cookies group by host_key order by c desc limit 8"):
    print(f"  {h}: {c}")
