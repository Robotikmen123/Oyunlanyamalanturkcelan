#!/usr/bin/env python3
"""Uretilen yamayi kaynakla karsilastirip regresyon arar.

Kontroller:
  1. Katlanmamis Turkce karakter kalmis mi (fontlar desteklemiyor)
  2. Markup etiketleri ([w:07], [font=..], [ATK]) kaynakla ayni mi
  3. \\r ve \\n kacis dizileri ayni sayida mi
  4. Satir ve CRLF sayilari ayni mi
"""
import os, re, sys
SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English"
OUT = "patch/tr/Resources/Lang/English"
TAG = re.compile(r"\[[^\]\n]*\]")
ESC = re.compile(r"\\[rn]")
UNFOLDED = set("ğĞşŞıİöÖüÜçÇâÂîÎûÛ")

def read(p): return open(p, "rb").read().decode("utf-8", errors="replace")

errs = []
checked = 0
for root, _, files in os.walk(OUT):
    for fn in sorted(files):
        dst = os.path.join(root, fn)
        rel = os.path.relpath(dst, OUT)
        src = os.path.join(SRC, rel)
        if not os.path.exists(src): continue
        a, b = read(src), read(dst)
        checked += 1
        leaked = UNFOLDED & set(b)
        if leaked:
            errs.append(f"{rel}: katlanmamis karakter {''.join(sorted(leaked))}")
        # etiketler: kaynakta olmayan yeni etiket veya kayip etiket
        ta, tb = sorted(TAG.findall(a)), sorted(TAG.findall(b))
        if ta != tb:
            errs.append(f"{rel}: markup etiketi farkli ({len(ta)} -> {len(tb)})")
        if len(ESC.findall(a)) != len(ESC.findall(b)):
            errs.append(f"{rel}: \\r/\\n sayisi farkli "
                        f"({len(ESC.findall(a))} -> {len(ESC.findall(b))})")
        if a.count("\n") != b.count("\n"):
            errs.append(f"{rel}: satir sayisi farkli")
        if a.count("\r") != b.count("\r"):
            errs.append(f"{rel}: CRLF sayisi farkli")

print(f"{checked} dosya kontrol edildi")
if errs:
    print(f"\n{len(errs)} SORUN:")
    for e in errs[:25]: print("  " + e)
    sys.exit(1)
print("temiz - tum kontroller gecti")
