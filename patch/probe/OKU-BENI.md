# Sonda Yaması — Lang sistemi canlı mı?

Amaç: 2 dakikada, oyunu oynamadan, `Resources/Lang/` klasörünün
gerçekten okunup okunmadığını anlamak.

## Kurulum

1. Oyunun klasörünü aç:
   `Dusttrust X ACT 1 (v1.1)\`
2. Önce **yedek al**:
   `Resources\Lang\English\OW Menu.txt` → `OW Menu.txt.yedek`
3. Bu klasördeki `Resources\Lang\English\OW Menu.txt` dosyasını
   oyundaki aynı yola kopyala (üzerine yaz).
4. `Dusttrust X.exe` çalıştır.

## Ne göreceksin

Oyun açılınca **dosya seçme ekranı** gelir. Orada şunlar değişmiş olmalı:

| İngilizce | Türkçe olmalı |
|---|---|
| SELECT A SAVE FILE | BIR KAYIT DOSYASI SEC |
| CONTINUE | DEVAM ET |
| Begin | Basla |
| Reset | Sifirla |
| ERASE | SIL |

Oyuna girip menüyü açarsan (ITEM/STAT/MENU satırı) orada da
ESYA / DURUM / MENU / KULLAN / BILGI / BIRAK görmelisin.

## Sonucu bana bildir

- **Değiştiyse** → Lang sistemi çalışıyor. Kalan ~1575 stringi çeviririm.
- **Değişmediyse** → Lang klasörü ölü. Metin `Dusttrust X.dat` içinde
  paketli, oraya girmemiz gerekir (çok daha büyük iş).
- **Oyun açılmıyor/hata veriyorsa** → yedeği geri koy, hatayı bana yaz.

## Notlar

- Türkçe karakterler bilerek ASCII'ye indirildi (ş→s, ğ→g, İ→I).
  Oyunun 9 fontunun hiçbirinde `ğ Ğ ş Ş İ` yok; ham Türkçe yazarsak
  boş kutu çıkar.
- Yer tutucular (`[Name]`, `[ATK]`, `[Gold]`...), `|` satır ayracı ve
  `[font=...]` etiketi olduğu gibi korundu.
