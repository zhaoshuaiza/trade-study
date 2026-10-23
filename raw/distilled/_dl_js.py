# -*- coding: utf-8 -*-
import urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
urls=[
 "https://cdn.weread.qq.com/web/wrwebnjlogic/js/app.6dde5475.js",
 "https://cdn.weread.qq.com/web/wrwebnjlogic/js/9.f252b488.js",
]
for u in urls:
    req=urllib.request.Request(u); req.add_header("User-Agent",UA)
    try:
        data=urllib.request.urlopen(req,timeout=40).read()
        fn=u.split("/")[-1]
        open(fn,"wb").write(data)
        print("saved",fn,len(data))
    except Exception as e:
        print("ERR",u,e)
