#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""尝试离线解密 Edge 的 weread cookie（DPAPI 主密钥 + AES-GCM）。
若能成功，就无需用户手动复制任何东西，直接拿到完整登录态。
"""
import json, base64, sqlite3, ctypes
from ctypes import wintypes
from Crypto.Cipher import AES

LS = r"C:\Users\admi\AppData\Local\Microsoft\Edge\User Data\Local State"
COOK = r"C:\Users\admi\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def dpapi_decrypt(data: bytes) -> bytes:
    blob_in = DATA_BLOB()
    buf = ctypes.create_string_buffer(data, len(data))
    blob_in.cbData = len(data)
    blob_in.pbData = ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))
    blob_out = DATA_BLOB()
    ok = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out))
    if not ok:
        raise ctypes.WinError(ctypes.windll.kernel32.GetLastError())
    out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return out


d = json.load(open(LS, encoding="utf-8"))
ek = base64.b64decode(d["os_crypt"]["encrypted_key"])
print("encrypted_key prefix:", ek[:8])
payload = ek[5:] if ek[:5] == b"DPAPI" else ek
try:
    master = dpapi_decrypt(payload)
    print("master key len:", len(master))
except Exception as e:
    print("DPAPI FAIL:", repr(e))
    raise SystemExit(1)

con = sqlite3.connect("file:" + COOK.replace("\\", "/") + "?mode=ro", uri=True)
rows = con.execute(
    "select name, encrypted_value from cookies where host_key like '%weread%'").fetchall()

out = {}
for name, enc in rows:
    if not enc or len(enc) < 16:
        print(f"  {name}: EMPTY")
        continue
    prefix = enc[:3]
    results = []
    for pfx, off in ((b"v10", 3), (b"v20", 3), (b"MSED", 5), (b"DPAPI", 5)):
        if enc[:len(pfx)] != pfx:
            continue
        nonce, ct = enc[off:off + 12], enc[off + 12:]
        try:
            pt = AES.new(master, AES.MODE_GCM, nonce=nonce).decrypt(ct)
            txt = pt.decode("utf-8", "ignore").rstrip("\x00")
            results.append((pfx.decode(), txt))
        except Exception as e:
            results.append((pfx.decode(), "ERR " + str(e)[:40]))
    if not results:
        print(f"  {name}: unknown prefix {prefix!r}")
        continue
    for pfx, txt in results:
        printable = "".join(ch for ch in txt if ch.isprintable())
        print(f"  {name} [{pfx}] -> {printable[:60]}")
        if name in ("wr_vid", "wr_skey", "wr_rt") and printable:
            out[name] = printable

print("\nEXTRACTED:", {k: (v[:12] + "..." if len(v) > 12 else v) for k, v in out.items()})
json.dump(out, open("_extracted_cookies.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
