---
name: icerik
description: DonerTrade için Türkçe B2B Instagram/TikTok/Facebook içeriği üretir — hook, Reels videosu, carousel, Story, açıklama ve haftalık yayın takvimi. Avrupa'daki gurbetçi döner toptancılarını hedefler.
---

# DonerTrade içerik üretimi

DonerTrade (donertrade.com), Avrupa'daki Türkçe konuşan toptancılara, distribütörlere ve ithalatçılara dondurulmuş döner satan bir B2B firmasıdır. Bu skill, onun sosyal medya içeriğini üretirken uyulacak kuralları ve yöntemi tarif eder.

## Hedef kitle
- **Kime:** Avrupa'daki gurbetçi döner toptancıları, dondurulmuş gıda toptancıları, et ithalatçıları, gıda distribütörleri, satın alma müdürleri. Tipik sipariş 5–10 ton ve üzeri.
- **Kime değil:** Türkiye (orada satış yok), tek tek restoranlar, tüketiciler, küçük perakende.
- Öncelikli ülkeler: Almanya, Hollanda, Belçika, Avusturya, Fransa, Polonya.

## Değişmez kurallar
1. Seyirciye giden her şey Türkçe. Toptancının başka bir profesyonelle konuşması gibi, "sen" diliyle; kurumsal ya da abartılı reklam dili yok.
2. **Teknik föy, laboratuvar testi ve pişirme firesinden bahsedilmez.**
3. Kanıtlanmamış ürün iddiası yok ("%100 but eti", "ilave su yok" vb.). Doğrulanmamış bir konu varsa iddia yerine alıcıya tavsiye çerçevesi kullanılır: "Tedarikçinden … iste / sor".
4. Rakip adı, markası ya da ürün görüntüsü kullanılmaz. Stok ya da yapay zekâ görüntüsü "bizim tesisimiz" gibi sunulmaz.
5. Her videonun sonunda: kendi DM anahtar kelimesi + minimum sipariş satırı + çerçeveli donertrade.com. (Mevcut videolarda "Minimum sipariş 5 ton" yazıyor; donertrade.com sitesinin "doğrulanmamış MOQ yayınlanmaz" kuralıyla uyum için karar bekliyor.)
6. Kırmızı et döner, tedariki kesinleşmeden videoda gösterilmez.
7. Higgsfield kredisi kullanıcı açıkça istemedikçe harcanmaz.
8. Video render edilmeden önce kullanıcı onayı alınır; kullanıcı "ver/geç" derse doğrudan üretilir.
9. Kullanıcı övgü istemez; değerlendirmeler dürüst ve gerekçeli olur.
10. donertrade.com sitesinin içerik kırmızı çizgileri sosyal medya için de geçerli: "kendi fabrikamız/tesisimiz/filomuz" yazılmaz, üretici adı geçmez, doğrulanmamış sertifika yazılmaz.

## Marka ve görsel şablon
- **Renkler:** zemin `#07090D`, ana kırık beyaz `#F2F1ED`, vurgu "döner altını" `#E2A54C`, kayıp/uyarı kırmızısı `#EB484D`, gri `#8C919B`, kart `#1B1D22`. Ürün çizimlerinde tavuk `#E8B862`, kırmızı et `#7A2822`.
- **Logo:** Kırık beyaz döner şişi ikonu + "DonerTrade" yazısı. Videoda sadece son karede ve küçük.
- **Font:** Inter Display Black/Bold, Inter SemiBold/Medium.
- **Format:** 1080×1920, 9:16, 30 fps, 12–15 sn. Tüm metin ortadaki 4:5 alanda (y ≈ 285–1635).
- **İlk kare:** Ana mesaj ilk karede tam görünür; siyah ekrandan belirme yok. En üstte küçük AB bayrağı + "Avrupa'da döner toptancısı mısın?" etiketi.
- **Akış:** hook (ilk kare) → problem/kayıp → somut rakam → ders → CTA kartı (kırık beyaz kutuda DM kelimesi).
- **Ses:** Seslendirme yoksa düşük dron + darbe, yazılarda "tık", sayaçlarda "pop". Paylaşırken platformun popüler müziği düşük sesle eklenir.
- Kod: eklenti klasöründeki `render/` (`tpl.py` şablon, `reels.py` sahneler, `static.py` carousel ve Story); logolar `brand/`, proje geçmişi `docs/arsiv_notu.md`. Eklenti kökü `${CLAUDE_PLUGIN_ROOT}`. Gerekenler: Python 3, Pillow, NumPy, FFmpeg, Inter fontları (`INTER_FONT_DIR`).

## Hook yazımı
- Para ya da zaman üzerinden, düz bir toptancı gerçeği; satış numarası yok. Her hook'ta "döner" kelimesi geçer.
- Kullanıcının beğendiği örnekler: "Döner toptancısının en pahalı hatası: sadece ton fiyatına bakmak." · "Ocak'taki döner şişiyle Haziran'daki şiş aynı olmalı." · "Ucuz döner alan toptancı, pahalı müşteri kaybeder."
- Rakamlarda kullanılan değerler: kilo başı 20 sent (ilk video) / 10 sent; restoran haftada 400 kg (≈ 21 ton/yıl); fiyat örneği 3,87 €/kg. Gerçek veri kullanılırsa kaynağı ekranda yazılır (ör. YouGov: Almanya'da et döner 2021'de 4,85 €, 2025'te 7,11 €, +%47).

## Algoritma ve yayın kuralları
- Instagram'ın en önemli üç sinyali: izlenme süresi, DM ile gönderilme, beğeni. Yeni kitleye ulaşmada en güçlüsü DM ile gönderilme → her açıklama "ortağına gönder" çağrısı içerir. Kaydetme için carousel.
- Sıklık: hafta içi her gün en fazla 1 Reels + haftada 1–2 carousel + günde 2–3 Story.
- Saatler (Orta Avrupa saati): 07:30, 12:30, 20:30 test edilir; sonra İstatistikler'deki en iyi saate geçilir.
- Konum: her paylaşımda farklı bir Avrupa şehri (Berlin, Köln, Amsterdam, Brüksel, Viyana, Duisburg…). Türkiye'yi kesin dışlamanın tek yolu reklamda ülke hariç tutma.
- Hashtag'ler ilk yoruma, 3–5 adet: #dönertoptan #dönertedarikçisi #gıdatoptancısı #dondurulmuşdöner #avrupadakitürkler #donertrade
- Aynı videolar Facebook Sayfası (Meta Business Suite ile planlı) ve TikTok işletme hesabında da paylaşılır. TikTok'a orijinal mp4 yüklenir, filigranlı dosya değil.

## Açıklama şablonu
```
<hook cümlesi>

<2–3 cümle: kayıp ve rakam>

Bu hesabı bilen bir ortağına gönder.

📩 <amaç> için DM'den <KELİME> yaz.
📦 Minimum sipariş: 5 ton
🌐 donertrade.com
```

## DM cevap şablonu
> Merhaba, yazdığın için teşekkürler. Doğru teklifi hazırlayabilmemiz için 3 kısa soru: 1) Firma adın ve şehrin? 2) Hangi ülkelere dağıtım yapıyorsun? 3) Aylık tahmini döner hacmin kaç ton? Cevabına göre en kısa sürede dönüyoruz.

5 ton ve üzeri cevaplar aynı gün telefon ya da WhatsApp ile aranır.

## Ölçüm
- Başarı ölçütü izlenme değil, Avrupa'dan gelen nitelikli DM.
- Haftalık bakılacaklar: ortalama izlenme süresi / video süresi, kaydırıp geçme oranı, Avrupa izleyici oranı, DM ile gönderilme, DM sayısı.
- İlk yayın (eski şablon): 131 izlenme, %73,5 kaydırıp geçme, %81,7 Türkiye. Ders: ilk kare dolu, kısa video, Avrupa sinyalleri.

## Bilinen zayıflıklar ve sıradaki iyileştirmeler
Sadece yazılı grafik videolar reklam gibi algılanır. En büyük kazanç sırasıyla: gerçek depo/palet/kamyon görüntüsü, başta 2 saniyelik kameraya konuşan bir yüz, insan sesi, somut ve risk taşımayan bir teklif (ör. ücretsiz numune kutusu).
