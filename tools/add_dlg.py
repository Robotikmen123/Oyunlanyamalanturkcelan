#!/usr/bin/env python3
"""Diyalog cevirilerini ortak kataloga ekler (parti parti calisilir).

Katalog tum Dialogue/ dosyalarina uygulanir; tekrar eden satirlar bir kez
cevrilir. stdin'den JSON {kaynak: ceviri} bekler.
"""
import json, os, sys
SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English/Dialogue"
P = "tools/catalog/dialogue.json"

new = json.load(sys.stdin)
shared = {}
if os.path.exists(P):
    cat = json.load(open(P, encoding="utf-8"))
    shared = next(iter(cat.values())) if cat else {}
shared.update(new)
cat = {f"Dialogue/{fn}": shared for fn in sorted(os.listdir(SRC))
       if fn.endswith((".txt", ".ini"))}
json.dump(cat, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"+{len(new)} eklendi, katalogda toplam {len(shared)}")
