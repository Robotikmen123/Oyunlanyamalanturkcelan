#!/usr/bin/env python3
"""Kaynak satirlari indeksle okuyup cevirilerle esler.

Anahtarlar dogrudan kaynak dosyadan alinir; elle yazmaktan dogan
kesme isareti / bosluk farki hatalari boylece imkansiz olur.
stdin: her satirda bir ceviri (kaynak araligiyla ayni sirada, ayni sayida).
"""
import json, sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
src = open("/tmp/dlg_uniq.txt", encoding="utf-8").read().split("\n")[lo-1:hi]
tr = [l for l in sys.stdin.read().split("\n") if l != ""]
if len(src) != len(tr):
    sys.exit(f"HATA: {len(src)} kaynak, {len(tr)} ceviri - sayilar tutmuyor")
# "=" satiri: kaynagi aynen koru (saf markup / cevrilecek metin yok).
# Boylece uzun yonerge dizilerini elle kopyalamak gerekmez.
out = {s: (s if t.strip() == "=" else t) for s, t in zip(src, tr)}
json.dump(out, sys.stdout, ensure_ascii=False)
