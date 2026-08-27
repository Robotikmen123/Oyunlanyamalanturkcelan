# Dusttrust X ACT 1 (v1.1) — Türkçe Yama

## Kurulum

1. Oyun klasöründeki `Resources\Lang\English\` yolunu **yedekle**.
2. Bu klasördeki `Resources\Lang\English\` içeriğini oyundaki aynı yola kopyala.
3. `Dusttrust X.exe` çalıştır.

## ÖNEMLİ: Önce bunu test et

Oyunun `Lang/` klasörünü gerçekten okuduğu **henüz kanıtlanmadı**. Aksini
gösteren dört işaret var (detay: PR açıklaması). Bu yüzden önce şuna bak:

Oyun açılınca **dosya seçme ekranı** gelir. `SELECT A SAVE FILE` yerine
`BIR KAYIT DOSYASI SEC` görüyorsan sistem çalışıyor demektir.

- **Değiştiyse** → yama tutuyor, çeviriye devam edilir.
- **Değişmediyse** → `Lang/` ölü. Metin `Dusttrust X.dat` içinde paketli,
  oraya girmek gerekir.

## Kapsam: TAMAMI çevrildi

| Bölüm | Dosya | Durum |
|---|---|---|
| Menü, başlık ve kayıt ekranı | 1 | tamam |
| Başarımlar | 1 | tamam |
| Eşyalar (isim, açıklama, kullanım) | 30 | tamam |
| Kayıt noktaları | 1 | tamam |
| Jenerik | 1 | tamam |
| Savaş | 1 | tamam |
| Diyaloglar | 90 | tamam |
| **Toplam** | **125** | **1400 benzersiz string** |

`python3 tools/missing.py` → 0 eksik token, 0 eksik dosya.

## Çeviri kararları

- **Türkçe karakterler ASCII'ye indirildi** (ş→s, ğ→g, İ→I). Zorunlu:
  oyunun 9 fontunun hepsinde `ğ Ğ ş Ş İ` eksik, dördünde `ı ö ü ç` de yok.
  Ham Türkçe yazılsa boş kutu render edilir.
- **`HP` `ATK` `DEF` `EXP` `LV` `ST` İngilizce bırakıldı.** `EXP` Undertale'de
  bir kelime oyunu (*EXecution Points*), `AT`/`DF` ise iki karakterlik dar
  alana sığıyor. Fan çevirilerinin yerleşik pratiği.
- **Karakter isimleri çevrilmedi** (Sans, Papyrus, Temmie, Napstaton).
- Savaş menüsündeki kısa eşya isimleri (`MonstDrink` → `CanavIcek`) orijinal
  karakter genişliğine sığdırıldı, hizalama bozulmuyor.

## Araçlar

- `tools/catalog/*.json` — çeviri kataloğu. Enjeksiyon mekanizmasından
  bağımsız: `Lang/` ölü çıkarsa aynı katalog `.dat` enjeksiyonunda kullanılır.
- `tools/apply.py` — katalogu kaynak dosyalara uygular, markup doğrular.
- `tools/verify.py` — üretilen yamayı kaynakla karşılaştırır (katlanmamış
  karakter, etiket/`\r`/`\n` sayısı, satır ve CRLF eşitliği).
- `tools/missing.py` — henüz çevrilmemiş tokenları listeler.

Yamayı yeniden üretmek için: `python3 tools/apply.py && python3 tools/verify.py`
