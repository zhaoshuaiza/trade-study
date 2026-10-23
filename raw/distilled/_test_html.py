import os, urllib.request
COOKIE = os.environ.get("WR_COOKIE")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
url="https://weread.qq.com/web/reader/33d32010813ab98e8g019623"
req=urllib.request.Request(url)
req.add_header("User-Agent",UA); req.add_header("Cookie",COOKIE); req.add_header("Referer","https://weread.qq.com/")
with urllib.request.urlopen(req,timeout=25) as r:
    html=r.read().decode("utf-8","ignore")
print("len",len(html))
import re
js=re.findall(r'src="([^"]+\.js)"',html)
for j in js[:20]: print(j)
