#!/usr/bin/env python3
"""Turkce metni oyunun fontlarinin destekledigi karakterlere indirger.

Oyunun 9 fontunun hicbirinde g-breve, s-cedilla ve noktali-I yok; bir kisminda
o/u/c umlaut-cedilla varyantlari da yok. Guvenli taraf: tam ASCII katlama.
"""
FOLD = {
    "ğ": "g", "Ğ": "G", "ş": "s", "Ş": "S", "ı": "i", "İ": "I",
    "ö": "o", "Ö": "O", "ü": "u", "Ü": "U", "ç": "c", "Ç": "C",
    "â": "a", "Â": "A", "î": "i", "Î": "I", "û": "u", "Û": "U",
}
# Fontlarin cogunda mevcut olanlar (secmeli katlama icin)
PRESENT_IN_MOST = set("öÖüÜçÇ")

def fold(text: str, keep_common: bool = False) -> str:
    out = []
    for ch in text:
        if keep_common and ch in PRESENT_IN_MOST:
            out.append(ch)
        else:
            out.append(FOLD.get(ch, ch))
    return "".join(out)

if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    sys.stdout.write(fold(data, keep_common="--keep" in sys.argv))
