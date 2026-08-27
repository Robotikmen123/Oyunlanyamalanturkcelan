#!/usr/bin/env python3
"""Diyalog cevirilerini ortak kataloga ekler (parti parti calisilir).

Katalog tum Dialogue/ dosyalarina uygulanir; tekrar eden satirlar bir kez
cevrilir. stdin'den JSON {kaynak: ceviri} bekler.

Markup imzasi kaynakla ayni olmayan ceviri kataloga HIC alinmaz.
"""
import json, os, re, sys

TAG = re.compile(r"\[[^\]\n]*\]")   # [w:07], [set.portrait:16], [effect:shake,1]
ESC = re.compile(r"\\[rn]")         # metin icindeki \r ve \n kacis dizileri

def sig(s):
    return sorted(TAG.findall(s)), len(ESC.findall(s))

SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English/Dialogue"
P = "tools/catalog/dialogue.json"

new = json.load(sys.stdin)
bad = [(e, t) for e, t in new.items() if sig(e) != sig(t)]
if bad:
    for e, t in bad:
        print(f"REDDEDILDI\n  kaynak: {e}\n  ceviri: {t}", file=sys.stderr)
    sys.exit(f"{len(bad)} ceviri markup uyusmazligi nedeniyle reddedildi")

shared = {}
if os.path.exists(P):
    cat = json.load(open(P, encoding="utf-8"))
    shared = next(iter(cat.values())) if cat else {}
shared.update(new)
cat = {f"Dialogue/{fn}": shared for fn in sorted(os.listdir(SRC))
       if fn.endswith((".txt", ".ini"))}
json.dump(cat, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"+{len(new)} eklendi, katalogda toplam {len(shared)}")
