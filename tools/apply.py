#!/usr/bin/env python3
"""Ceviri katalogunu kaynak Lang dosyalarina uygular.

Mimari: katalog (JSON) ceviriyi enjeksiyon mekanizmasindan ayirir. Ayni katalog
ileride .dat enjeksiyonu icin de kullanilabilir.

Katalog TAM token eslesmesi kullanir: anahtar kaynak metnin aynisi, deger ise
ayni markup'i tasiyan Turkce karsiligi. Boylece kirilgan "koru/geri koy"
katmanina gerek kalmaz. Uygulamadan once her ceviri markup acisindan dogrulanir.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fold_tr import fold

SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English"
OUT = "/home/user/Oyunlanyamalanturkcelan/patch/tr/Resources/Lang/English"
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog")

TAG = re.compile(r"\[[^\]\n]*\]")          # [font=..], [w:07], [ATK], [italic]
BREAK = re.compile(r"\\[rn]")               # \\r kutu ici satir, \\n yeni kutu

# .ini icinde sadece bu anahtarlarin degeri cevrilir
TR_KEYS = {"Name","UseText","InfoText","SansText","DropText","PUseText",
           "Check","AttackText"}
PAD = re.compile(r"^(.*?)([\s,]*)$", re.S)   # "Apple     ," -> govde + hizalama eki

def markup_sig(s):
    """Bir metnin markup imzasi: etiketler + \\r sayisi."""
    return (tuple(TAG.findall(s)), len(BREAK.findall(s)))

def validate(cat, path):
    """Her cevirinin kaynakla ayni markup'i tasidigini dogrular."""
    bad = []
    for en, tr in cat.items():
        if markup_sig(en) != markup_sig(tr):
            bad.append((en, tr))
    if bad:
        print(f"HATA {path}: {len(bad)} ceviride markup uyusmazligi")
        for en, tr in bad[:5]:
            print(f"  kaynak: {en[:70]}\n  ceviri: {tr[:70]}")
    return not bad

def apply_ini(rel, cat):
    """key=value satirlarinda yalnizca cevrilebilir anahtarlarin degerini cevirir.
    Hizalama eki (sondaki bosluk/virgul) korunur ve genislik esitlenir."""
    raw = open(os.path.join(SRC, rel), "rb").read().decode("utf-8", errors="replace")
    hit = tot = 0
    out = []
    for line in raw.split("\n"):
        eol = "\r" if line.endswith("\r") else ""   # CRLF satir sonunu koru
        m = re.match(r"^([A-Za-z0-9_]+)=(.*)$", line[:len(line)-len(eol)])
        if not m or m.group(1) not in TR_KEYS or not m.group(2).strip():
            out.append(line); continue
        key, val = m.group(1), m.group(2)
        body, pad = PAD.match(val).groups()
        tot += 1
        if body in cat:
            tr = fold(cat[body])
            # orijinal genisligi koru (savas menusu hizalamasi)
            if pad and len(tr) < len(body) + len(pad):
                tr += " " * (len(body) + len(pad) - len(tr) - len(pad.strip()))
            out.append((f"{key}={tr}{pad.strip()}" if pad.strip()
                        else f"{key}={tr}{pad}") + eol)
            hit += 1
        else:
            out.append(line)
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write("\n".join(out).encode("utf-8"))
    return hit, tot

def apply_file(rel, cat):
    if rel.endswith(".ini"):
        return apply_ini(rel, cat)
    src = os.path.join(SRC, rel)
    raw = open(src, "rb").read().decode("utf-8")
    parts = re.split(r"(\||\r\n|\n)", raw)
    hit = 0
    out = []
    for p in parts:
        if p in ("|", "\r\n", "\n"):
            out.append(p); continue
        stripped = p.strip()
        if stripped in cat:
            # cevresindeki bosluklari koru
            out.append(p.replace(stripped, fold(cat[stripped]))); hit += 1
        else:
            out.append(p)
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write("".join(out).encode("utf-8"))
    total = sum(1 for p in parts if p not in ("|", "\r\n", "\n") and p.strip())
    return hit, total

def main():
    ok = True
    grand_h = grand_t = 0
    for f in sorted(os.listdir(CAT)):
        if not f.endswith(".json"): continue
        data = json.load(open(os.path.join(CAT, f), encoding="utf-8"))
        for rel, cat in data.items():
            if not validate(cat, rel): ok = False; continue
            h, t = apply_file(rel, cat)
            grand_h += h; grand_t += t
            print(f"{rel:34s} {h:4d}/{t:4d} token cevrildi")
    print(f"\nTOPLAM: {grand_h}/{grand_t}")
    return 0 if ok else 1

sys.exit(main())
