#!/usr/bin/env python3
"""Sonda yamasi: Lang sisteminin canli olup olmadigini oyunda gozle test eder.

Token bazli: metin '|' ve satir sonlarina gore parcalanir, sadece TAM eslesen
parcalar cevrilir. Boylece 'ERASE' -> 'REALLY ERASE?' gibi substring cakismalari
olmaz. Yer tutucular ([Name], [ATK]...) ve [font=] etiketi hic dokunulmaz.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fold_tr import fold

SRC = "/home/user/dt/game/Dusttrust X ACT 1 (v1.1)/Resources/Lang/English"
OUT = "/home/user/Oyunlanyamalanturkcelan/patch/probe/Resources/Lang/English"

EXACT = {
    "ITEM": "ESYA", "STAT": "DURUM", "MENU": "MENU", "USE": "KULLAN",
    "INFO": "BILGI", "DROP": "BIRAK", "EMPTY": "BOS", "RETURN": "GERI DON",
    "SELECT A SAVE FILE": "BIR KAYIT DOSYASI SEC", "CONTINUE": "DEVAM ET",
    "Reset": "Sıfırla", "Begin": "Başla", "Continue": "Devam Et",
    "SELECT A FILE TO ERASE.": "SILINECEK DOSYAYI SEC.", "ERASE": "SIL",
    "REALLY ERASE?": "GERÇEKTEN SILINSIN MI?", "DO NOT": "HAYIR",
    "Save": "Kaydet", "Return": "Geri Dön", "File saved.": "Dosya kaydedildi.",
    "Yes": "Evet", "No": "Hayır",
    "* Return to Title Screen?": "* Başlık ekranına dönülsün mü?",
    "YES (RESTART": "EVET (YENİDEN", "REQUIRED)": "BAŞLATMA GEREKİR)",
}
# Bosluklu tek satirda birden fazla etiket (ornek: "   Yes      No")
INLINE = [("Yes", "Evet"), ("No", "Hayır")]
# Yer tutucu iceren satirlar icin onek cevirisi
PREFIX = [("ASHED:", "KUL EDILEN:"), ("SPARED:", "BAĞIŞLANAN:"),
          ("WEAPON:", "SILAH:"), ("ARMOR:", "ZIRH:"), ("GOLD:", "ALTIN:"),
          ("EXP:", "DEN:"), ("AT ", "SL "), ("DF ", "SV ")]

def tr_token(tok):
    stripped = tok.strip()
    if stripped in EXACT:
        return tok.replace(stripped, fold(EXACT[stripped]))
    for en, tr in PREFIX:
        if stripped.startswith(en):
            return tok.replace(en, fold(tr), 1)
    # bosluk hizasi korunarak satir ici kelime degisimi
    if re.search(r"\bYes\b", tok) and re.search(r"\bNo\b", tok):
        for en, tr in INLINE:
            tok = re.sub(rf"\b{en}\b", fold(tr), tok)
    return tok

def main():
    os.makedirs(OUT, exist_ok=True)
    raw = open(os.path.join(SRC, "OW Menu.txt"), "rb").read().decode("utf-8")
    # '|' ve satir sonlarini ayirici olarak koru
    parts = re.split(r"(\||\r\n|\n)", raw)
    out = "".join(p if p in ("|", "\r\n", "\n") else tr_token(p) for p in parts)
    open(os.path.join(OUT, "OW Menu.txt"), "wb").write(out.encode("utf-8"))
    n = sum(1 for p in parts if p not in ("|", "\r\n", "\n") and tr_token(p) != p)
    print(f"OW Menu.txt yazildi - {n} parca cevrildi")

main()
