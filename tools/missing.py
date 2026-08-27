#!/usr/bin/env python3
"""Henuz cevrilmemis tokenlari listeler. Ceviri isini yonetmek icin."""
import json, os, re, sys
SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English"
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog")

# Cevrilmeyecekler: saf markup, sayi, yer tutucu, gelistirici notu
SKIP = re.compile(r"""^(
      \[[^\]]*\]                # sadece etiket
    | [\s\W\d]*                 # noktalama/sayi/bosluk
    | \(room\ was\ cut\)        # gelistirici yer tutucusu
    | \*?\s*TEXT
)$""", re.X)

def load_cat():
    known = set()
    for f in os.listdir(CAT):
        if f.endswith(".json"):
            for rel, c in json.load(open(os.path.join(CAT,f),encoding="utf-8")).items():
                known |= set(c.keys())
    return known

TR_KEYS = {"Name","UseText","InfoText","SansText","DropText","PUseText",
           "Check","AttackText"}

def tokens(path):
    """.ini icin sadece cevrilebilir anahtarlarin DEGERI, .txt icin tokenlar."""
    raw = open(path,"rb").read().decode("utf-8",errors="replace")
    if path.endswith(".ini"):
        for line in raw.split("\n"):
            m = re.match(r"^([A-Za-z0-9_]+)=(.*)$", line.rstrip("\r"))
            if m and m.group(1) in TR_KEYS and m.group(2).strip():
                v = re.match(r"^(.*?)[\s,]*$", m.group(2), re.S).group(1)
                if v and not SKIP.match(v):
                    yield v
        return
    for p in re.split(r"\||\r\n|\n", raw):
        s = p.strip()
        if s and not SKIP.match(s):
            yield s

def main():
    known = load_cat()
    only = sys.argv[1] if len(sys.argv)>1 else ""
    rows=[]
    for root,_,files in os.walk(SRC):
        for fn in sorted(files):
            if not fn.endswith((".txt",".ini")): continue
            rel = os.path.relpath(os.path.join(root,fn), SRC)
            if only and only not in rel: continue
            miss = [t for t in tokens(os.path.join(root,fn)) if t not in known]
            if miss: rows.append((rel, miss))
    total = sum(len(m) for _,m in rows)
    if only:
        for rel,miss in rows:
            print(f"--- {rel} ({len(miss)}) ---")
            for m in miss: print(m)
    else:
        for rel,miss in sorted(rows, key=lambda r:-len(r[1]))[:20]:
            print(f"{len(miss):5d}  {rel}")
        print(f"\nEKSIK TOPLAM: {total} token, {len(rows)} dosya")
main()
