"""Carousel (1080x1350) and Story backgrounds (1080x1920) in brand palette."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import *
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "static")
os.makedirs(OUT, exist_ok=True)
CW, CH = 1080, 1350

def bg(w, h):
    im = Image.new("RGBA", (w, h), BG + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, w, 90): d.line([(x, 0), (x, h)], fill=(15, 17, 22, 255))
    for y in range(0, h, 90): d.line([(0, y), (w, y)], fill=(15, 17, 22, 255))
    return im

def T(c, txt, font, col, x, y, anchor="mt"):
    ImageDraw.Draw(c).text((x, y), txt, font=font, fill=col + (255,), anchor=anchor)

def wrap(txt, font, maxw):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if font.getlength(test) <= maxw: cur = test
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def footer(c, page, total):
    h = c.height
    T(c, "donertrade.com", BOLD(36), CREAM, 80, h-90, "lm")
    T(c, f"{page}/{total}", BOLD(36), GREY, c.width-80, h-90, "rm")

def small_logo(c, y=70):
    im = Image.open(os.path.join(R.BRAND, "logo_word.png")).convert("RGBA"); im = im.crop(im.getbbox())
    hh = 40; im = im.resize((int(im.width*hh/im.height), hh), Image.LANCZOS)
    c.alpha_composite(im, (80, y))

QS = [
    ("Referans gösterebilir misin?", "Aynı ülkede çalıştığın bir toptancı var mı?"),
    ("Şiş ağırlığı toleransın ne?", "Kaç gram sapma kabul ediliyor?"),
    ("Reçete değişirse haber veriyor musun?", "Önceden ve yazılı olarak mı?"),
    ("Her partinin numarası var mı?", "Sorun çıkınca hangi parti olduğu bulunabiliyor mu?"),
    ("Sıcaklık kaydı veriyor musun?", "Sevkiyat boyunca soğuk zincir kayıtlı mı?"),
    ("Teslim süren yazılı mı?", "Gecikirse ne oluyor?"),
    ("Numune gönderiyor musun?", "Kendi fırınında denemeden 10 ton alma."),
    ("Hatalı partide iade nasıl işliyor?", "Kim karar veriyor, kim ödüyor?"),
    ("Hangi ülkelere teslim ediyorsun?", "Kendi aracınla mı, nakliyeciyle mi?"),
    ("Fiyat kaç ay sabit?", "Minimum sipariş ve ödeme koşulları ne?"),
]

def carousel():
    total = 7
    # cover
    c = bg(CW, CH)
    mini_eu(c, 80 + 33, 140, 66); T(c, "Avrupa'daki döner toptancıları için", SEMI(40), CREAM, 170, 140, "lm")
    y = 330
    for ln, col in [("Döner tedarikçine", WHITE), ("bu 10 soruyu", WHITE), ("sormadan", GOLD), ("10 ton alma.", GOLD)]:
        T(c, ln, BLACK(110), col, 80, y, "lt"); y += 130
    T(c, "Kaydet. Ortağına gönder. →", BOLD(52), CREAM, 80, y+60, "lt")
    footer(c, 1, total); c.convert("RGB").save(os.path.join(OUT, "Carousel_01.png"))
    # question slides
    for s in range(5):
        c = bg(CW, CH); small_logo(c)
        y = 230
        for k in range(2):
            n = s*2 + k + 1; q, sub = QS[n-1]
            rrect_c = ImageDraw.Draw(c)
            rrect_c.rounded_rectangle((80, y, 80+130, y+130), radius=30, fill=CREAM + (255,))
            T(c, f"{n}", BLACK(84), BG, 145, y+65, "mm")
            ly = y + 10
            for ln in wrap(q, BLACK(66), 700):
                T(c, ln, BLACK(66), WHITE, 250, ly, "lt"); ly += 80
            for ln in wrap(sub, SEMI(44), 700):
                T(c, ln, SEMI(44), GREY, 250, ly+10, "lt"); ly += 56
            y = max(ly + 120, y + 420)
        footer(c, s+2, total); c.convert("RGB").save(os.path.join(OUT, f"Carousel_{s+2:02d}.png"))
    # closing
    c = bg(CW, CH)
    y = 260
    for ln, col in [("Bu 10 soruyu", WHITE), ("DonerTrade'e", GOLD), ("de sor.", WHITE)]:
        T(c, ln, BLACK(110), col, CW//2, y, "mt"); y += 135
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((CW/2-360, y+60, CW/2+360, y+250), radius=36, fill=CREAM + (255,))
    T(c, "DM: SORU", BLACK(110), BG, CW//2, y+155, "mm")
    T(c, "Minimum sipariş 5 ton", SEMI(50), WHITE, CW//2, y+310, "mt")
    im = Image.open(os.path.join(R.BRAND, "logo_full.png")).convert("RGBA"); im = im.crop(im.getbbox())
    hh = 170; im = im.resize((int(im.width*hh/im.height), hh), Image.LANCZOS)
    c.alpha_composite(im, (int(CW/2 - im.width/2), y+400))
    footer(c, 7, total); c.convert("RGB").save(os.path.join(OUT, "Carousel_07.png"))

# ---------- stories (1080x1920; sticker area left empty) ----------
def story(name, lines, sticker_hint, sticker_y=1000, sticker_h=330):
    c = bg(1080, 1920); small_logo(c, y=260)
    y = 420
    for txt, font, col in lines:
        for ln in wrap(txt, font, 900):
            T(c, ln, font, col, 540, y, "mt"); y += int(font.size*1.18)
        y += 20
    T(c, "donertrade.com", BOLD(42), CREAM, 540, 1560, "mm")
    c.convert("RGB").save(os.path.join(OUT, name))

def stories():
    story("Story_Gun1_Anket_Ulke.png",
          [("Hangi ülkede", BLACK(100), WHITE), ("döner toptancısısın?", BLACK(88), GOLD)],
          "[ANKET çıkartması: Almanya / Hollanda / Belçika / Diğer]")
    story("Story_Gun2_Anket_TedarikciDegisimi.png",
          [("Son 1 yılda", BLACK(100), WHITE), ("döner tedarikçini", BLACK(92), GOLD), ("değiştirdin mi?", BLACK(92), GOLD)],
          "[ANKET çıkartması: Evet / Hayır]")
    story("Story_Gun3_Quiz_DonerFiyati.png",
          [("Almanya'da et dönerin", BLACK(84), WHITE), ("2025 ortalama fiyatı?", BLACK(84), GOLD),
           ("Kaynak: YouGov", MED(36), GREY)],
          "[TEST çıkartması: 5,90 € / 7,11 € (doğru) / 8,50 €]")
    story("Story_Gun4_Soru_Tedarikci.png",
          [("Toptancılar:", BLACK(96), WHITE), ("Tedarikçinde seni en çok ne kızdırıyor?", BLACK(76), GOLD)],
          "[SORU çıkartması: \"Yaz, cevaplayalım\"]")
    story("Story_Gun5_Kaydirici_Fiyat.png",
          [("Bu kış döner", BLACK(96), WHITE), ("satışların nasıl gidiyor?", BLACK(84), GOLD)],
          "[EMOJİ KAYDIRICI çıkartması — döner emojisi]")
    story("Story_Gun6_Anket_Hacim.png",
          [("Aylık kaç ton", BLACK(100), WHITE), ("döner alıyorsun?", BLACK(96), GOLD)],
          "[ANKET çıkartması: 1–5 ton / 5–10 ton / 10+ ton]")
    story("Story_Gun7_DM_Cagri.png",
          [("Bu hafta 5 video,", BLACK(92), WHITE), ("1 soru listesi paylaştık.", BLACK(80), WHITE),
           ("Sorun varsa yaz.", BLACK(96), GOLD)],
          "[BAĞLANTI veya DM çıkartması]")

if __name__ == "__main__":
    carousel(); stories()
    print(sorted(os.listdir(OUT)))
