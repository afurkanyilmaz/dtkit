import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
os.makedirs(OUT, exist_ok=True)

# =============== R1: Trend — döner fiyatı %47 (YouGov) — DM: FİYAT ===============
def t1(t):
    c = new_canvas(); top_label(c)
    text_layer(c, "Almanya'da döner", BLACK(100), WHITE, W//2, 520, 1.0)
    text_layer(c, "4 yılda", BLACK(100), WHITE, W//2, 640, 1.0)
    z = 1.0 + 0.06*(1 - eo(prog(t, 0.0, 0.5)))
    f = BLACK(int(230*z))
    text_layer(c, "%47", f, GOLD, W//2, 860, 1.0, anchor="mm")
    text_layer(c, "pahalandı.", BLACK(100), WHITE, W//2, 990, 1.0)
    text_layer(c, "Et döner ortalaması · Kaynak: YouGov", MED(34), GREY, W//2, 1140, 1.0)
    return c

def t2(t):
    c = new_canvas()
    text_layer(c, "Et döner ortalama fiyatı", BOLD(60), GREY, W//2, 400, 1.0)
    base = 1180; maxh = 560
    for i, (yr, val, col, st) in enumerate([("2021", 4.85, GREY, 0.1), ("2025", 7.11, GOLD, 0.5)]):
        p = eo(prog(t, st, 0.8)); h = maxh*val/7.11*p
        x = W/2 - 260 + i*300
        rrect(c, (x, base-h, x+220, base), col, radius=18, alpha=1.0 if p > 0 else 0)
        v = val*p
        if p > 0:
            text_layer(c, f"{v:.2f} €".replace(".", ","), BLACK(64), WHITE, x+110, base-h-80, 1.0)
        text_layer(c, yr, BOLD(52), WHITE, x+110, base+30, 1.0)
    return c

def t3(t):
    c = new_canvas()
    text_layer(c, "Müşteri artık", BLACK(104), WHITE, W//2, 520, 1.0)
    text_layer(c, "daha çok ödüyor.", BLACK(104), WHITE, W//2, 640, 1.0)
    reveal(c, "Daha çok", BLACK(110), GOLD, 830, t, 0.7)
    reveal(c, "sorguluyor.", BLACK(110), GOLD, 950, t, 0.85)
    return c

def t4(t):
    c = new_canvas()
    text_layer(c, "7 € ödeyen müşteri", BLACK(96), WHITE, W//2, 520, 1.0)
    text_layer(c, "kötü döneri", BLACK(110), RED, W//2, 650, 1.0)
    text_layer(c, "affetmez.", BLACK(110), RED, W//2, 775, 1.0)
    reveal(c, "Restoran da toptancısını.", BLACK(76), GREY, 980, t, 0.9)
    return c

def t5(t):
    c = new_canvas(url=False); cta(c, t, "Fiyat-kalite görüşmesi", "için DM'den yaz:", "FİYAT")
    return c

R1 = ([(t1, 3.0), (t2, 2.8), (t3, 2.6), (t4, 2.8), (t5, 3.0)],
      [(0, 0, kick(1.0, 0.5)), (0, 0.05, tick()),
       (1, 0.1, low(0.25)), (1, 0.5, low(0.25)), (1, 1.3, kick(0.8, 0.4)),
       (2, 0.0, tick()), (2, 0.7, kick(0.7, 0.35)), (2, 0.85, tick()),
       (3, 0.0, kick(0.9, 0.45)), (3, 0.9, tick()),
       (4, 0.0, kick(1.0, 0.5)), (4, 0.2, chime())])

# =============== R2: Video 2 — H21 — DM: HESAP ===============
def a1(t):
    c = new_canvas(); top_label(c)
    text_layer(c, "Döner toptancısının", BLACK(92), WHITE, W//2, 500, 1.0)
    text_layer(c, "en pahalı hatası:", BLACK(100), RED, W//2, 615, 1.0)
    p = 1 - 0.0
    rrect(c, (W/2-300, 790, W/2+300, 960), CARD, radius=32, alpha=1.0, outline=RED, width=5)
    text_layer(c, "€ / ton", BLACK(110), WHITE, W//2, 875, 1.0, anchor="mm")
    text_layer(c, "Sadece ton fiyatına bakmak.", BOLD(66), WHITE, W//2, 1020, 1.0)
    line(c, W/2-300, 1110, W/2+300, GOLD, 6, eo(prog(t, 0.4, 0.5)))
    return c

ROWS2 = [("Ton fiyatı", "faturada", GREY), ("+ İade", "yazmaz", RED), ("+ Kaybedilen müşteri", "yazmaz", RED)]
def a2(t):
    c = new_canvas()
    text_layer(c, "Dönerin gerçek maliyeti", BLACK(80), WHITE, W//2, 380, 1.0)
    for i, (lab, note, col) in enumerate(ROWS2):
        p = eo(prog(t, 0.1 + i*0.4, 0.3)); y = 540 + i*175 + (1-p)*24
        rrect(c, (110, y, 970, y+140), CARD, radius=26, alpha=p)
        text_layer(c, lab, BOLD(58), WHITE, 150, y+70, p, anchor="lm")
        text_layer(c, note, MED(40), col, 930, y+70, p, anchor="rm")
    line(c, W/2-430, 1080, W/2+430, GREY, 5, eo(prog(t, 1.3, 0.3)))
    reveal(c, "= Gerçek maliyet", BLACK(100), RED, 1110, t, 1.5)
    return c

def a3(t):
    c = new_canvas()
    text_layer(c, "Ucuz döner", BLACK(96), WHITE, W//2, 420, 1.0)
    text_layer(c, "bir kez kâr ettirir.", BLACK(86), GOLD, W//2, 535, 1.0)
    reveal(c, "Kaybettiğin müşteri", BLACK(84), WHITE, 720, t, 0.5)
    reveal(c, "her ay zarar ettirir.", BLACK(84), RED, 825, t, 0.7)
    months_row(c, t, 1.2, y=1000)
    return c

def a4(t):
    c = new_canvas(url=False); cta(c, t, "Toplam maliyet tablosu", "için DM'den yaz:", "HESAP")
    return c

R2 = ([(a1, 3.0), (a2, 3.0), (a3, 3.2), (a4, 3.0)],
      [(0, 0, kick(1.0, 0.5)), (0, 0.4, tick()),
       (1, 0.0, tick()), (1, 0.1, low()), (1, 0.5, low()), (1, 0.9, low()), (1, 1.5, kick(0.9, 0.45)),
       (2, 0.0, tick()), (2, 0.5, tick()), (2, 0.7, tick())] + [(2, 1.2 + i*0.08, low(0.14)) for i in range(12)] +
      [(3, 0.0, kick(1.0, 0.5)), (3, 0.2, chime())])

# =============== R3: Video 7 — H67 — DM: SENT ===============
def b1(t):
    c = new_canvas(); top_label(c)
    text_layer(c, "Dönerde kilo başı", BLACK(92), WHITE, W//2, 500, 1.0)
    text_layer(c, "10 sent ucuz.", BLACK(110), GOLD, W//2, 615, 1.0)
    rrect(c, (110, 800, 970, 1000), CARD, radius=32, alpha=1.0)
    text_layer(c, "–0,10 € / kg", BLACK(116), GOLD, W//2, 900, 1.0, anchor="mm")
    text_layer(c, "= –100 € / ton", BLACK(104), WHITE, W//2, 1060, 1.0)
    line(c, W/2-330, 1185, W/2+330, GOLD, 6, eo(prog(t, 0.4, 0.5)))
    return c

def b2(t):
    c = new_canvas()
    text_layer(c, "10 tonda", BLACK(100), WHITE, W//2, 470, 1.0)
    v = 1000*eo(prog(t, 0.0, 0.9))
    s = f"{int(round(v)):,}".replace(",", ".")
    text_layer(c, f"{s} €", BLACK(220), GOLD, W//2, 600, 1.0)
    reveal(c, "Kulağa iyi geliyor.", BLACK(84), GREY, 930, t, 1.0)
    return c

def b3(t):
    c = new_canvas()
    text_layer(c, "Ama o ucuz döner yüzünden", BLACK(72), WHITE, W//2, 380, 1.0)
    text_layer(c, "bir restoran giderse...", BLACK(84), RED, W//2, 480, 1.0)
    out = eio(prog(t, 0.3, 0.8))
    tint = tuple(int(CARD[i] + (RED[i]*0.55 - CARD[i])*prog(t, 0.1, 0.3)) for i in range(3))
    restaurant_card(c, 110 + out*1100, 640, "Restoran C", "400 kg/hafta", alpha=1.0, tint=tint)
    reveal(c, "kaybın 1.000 €'da bitmez.", BLACK(80), WHITE, 860, t, 1.0)
    months_row(c, t, 1.4, y=1000)
    reveal(c, "Her ay devam eder.", BLACK(84), RED, 1170, t, 2.3)
    return c

def b4(t):
    c = new_canvas()
    text_layer(c, "Sentle değil,", BLACK(110), WHITE, W//2, 560, 1.0)
    reveal(c, "müşterinin kalmasıyla", BLACK(90), GOLD, 700, t, 0.25)
    reveal(c, "hesap yap.", BLACK(110), GOLD, 820, t, 0.45)
    return c

def b5(t):
    c = new_canvas(url=False); cta(c, t, "Teklif için", "DM'den yaz:", "SENT")
    return c

R3 = ([(b1, 2.8), (b2, 2.4), (b3, 3.4), (b4, 2.0), (b5, 3.0)],
      [(0, 0, kick(1.0, 0.5)), (0, 0.4, tick())] +
      [(1, 0.0, kick(0.6, 0.3))] + [(1, k*0.06, tick(0.08)) for k in range(15)] + [(1, 1.0, tick())] +
      [(2, 0.0, tick()), (2, 0.3, whoosh()), (2, 1.0, tick())] + [(2, 1.4 + i*0.08, low(0.14)) for i in range(12)] +
      [(2, 2.3, kick(0.9, 0.45)), (3, 0.0, tick()), (3, 0.25, tick()), (3, 0.45, kick(0.7, 0.35)),
       (4, 0.0, kick(1.0, 0.5)), (4, 0.2, chime())])

# =============== R4: Video 12 — H74 — DM: TUTARLI ===============
MEAT = (196, 128, 78); MEAT_D = (150, 92, 52)
def spit(c, cx, top, h):
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    wt, wb = 150, 95
    d.line([(cx, top-30), (cx, top+h+40)], fill=(170, 175, 185, 255), width=10)
    d.polygon([(cx-wt/2, top), (cx+wt/2, top), (cx+wb/2, top+h), (cx-wb/2, top+h)], fill=MEAT + (255,))
    for k in range(1, 7):
        y = top + h*k/7; w = wt + (wb-wt)*k/7
        d.line([(cx-w/2+6, y), (cx+w/2-6, y)], fill=MEAT_D + (255,), width=5)
    c.alpha_composite(lay)

def c1(t):
    c = new_canvas(); top_label(c)
    yy, xx = np.mgrid[0:H:4, 0:W:4]
    m = np.clip(1 - np.sqrt((xx-W/2)**2 + (yy-640)**2)/380, 0, 1)**1.5
    glow = Image.new("RGBA", (W, H), GOLD + (0,)); glow.putalpha(Image.fromarray((m*60).astype(np.uint8), "L").resize((W, H)))
    c.alpha_composite(glow)
    spit(c, W/2, 500, 280)
    text_layer(c, "Döner kalitesini", BLACK(100), WHITE, W//2, 870, 1.0)
    text_layer(c, "bir kez satarsın.", BLACK(100), WHITE, W//2, 985, 1.0)
    reveal(c, "Tutarlılığını her ay.", BLACK(96), GOLD, 1130, t, 0.6)
    return c

def c2(t):
    c = new_canvas()
    text_layer(c, "İlk numune", BLACK(100), WHITE, W//2, 380, 1.0)
    text_layer(c, "herkesin iyidir.", BLACK(100), WHITE, W//2, 495, 1.0)
    cols, cw, chh, gap = 6, 140, 110, 16; x0 = W/2 - (cols*cw + (cols-1)*gap)/2
    for i in range(12):
        r, k = divmod(i, cols); x = x0 + k*(cw+gap); y = 680 + r*(chh+gap)
        q = eo(prog(t, 0.1 + i*0.05, 0.2)); hl = prog(t, 1.1, 0.3) if i == 11 else 0
        rrect(c, (x, y, x+cw, y+chh), (60, 46, 26) if hl else CARD, radius=16, alpha=q, outline=GOLD if hl > 0.3 else None, width=5)
        text_layer(c, f"{i+1}.", BOLD(46), GOLD if hl > 0.3 else WHITE, x+cw/2, y+chh/2, q, anchor="mm")
    reveal(c, "12. teslimat da öyle mi?", BLACK(84), GOLD, 1000, t, 1.3)
    return c

def c3(t):
    c = new_canvas()
    text_layer(c, "Tutarlılık demek:", BLACK(100), WHITE, W//2, 380, 1.0)
    for i, r in enumerate(["Aynı reçete", "Aynı şiş ağırlığı", "Aynı soğuk zincir"]):
        p = eo(prog(t, 0.1 + i*0.35, 0.3)); y = 580 + i*180 + (1-p)*24
        rrect(c, (110, y, 970, y+140), CARD, radius=28, alpha=p)
        text_layer(c, r, BOLD(60), WHITE, 150, y+70, p, anchor="lm")
        rrect(c, (720, y+35, 930, y+105), (60, 46, 26), radius=35, alpha=p, outline=GOLD, width=3)
        text_layer(c, "her ay", BOLD(40), GOLD, 825, y+70, p, anchor="mm")
    return c

def c4(t):
    c = new_canvas()
    text_layer(c, "Tedarikçine sor:", BLACK(96), WHITE, W//2, 470, 1.0)
    reveal(c, "“12. teslimatı", BLACK(100), GOLD, 620, t, 0.15)
    reveal(c, "nasıl garanti", BLACK(100), GOLD, 740, t, 0.3)
    reveal(c, "ediyorsun?”", BLACK(100), GOLD, 860, t, 0.45)
    return c

def c5(t):
    c = new_canvas(url=False); cta(c, t, "Yıllık tedarik görüşmesi", "için DM'den yaz:", "TUTARLI", word_size=140)
    return c

R4 = ([(c1, 3.0), (c2, 3.0), (c3, 2.4), (c4, 2.4), (c5, 3.0)],
      [(0, 0, kick(1.0, 0.5)), (0, 0.6, kick(0.6, 0.3)),
       (1, 0.0, tick())] + [(1, 0.1 + i*0.05, pop(0.1)) for i in range(12)] + [(1, 1.1, kick(0.8, 0.4)), (1, 1.3, tick()),
       (2, 0.0, tick())] + [(2, 0.1 + i*0.35, pop(0.25)) for i in range(3)] +
      [(3, 0.0, tick()), (3, 0.15, tick()), (3, 0.3, tick()), (3, 0.45, kick(0.7, 0.35)),
       (4, 0.0, kick(1.0, 0.5)), (4, 0.2, chime())])

REELS = {
    "R1": (R1, "Gun1_Reel_DonerFiyati_FIYAT.mp4"),
    "R2": (R2, "Gun5_Reel_EnPahaliHata_HESAP.mp4"),
    "R3": (R3, "Gun6_Reel_10Sent_SENT.mp4"),
    "R4": (R4, "Gun7_Reel_Tutarlilik_TUTARLI.mp4"),
}

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "stills":
        for k, ((scenes, _), _) in REELS.items():
            stills(os.path.join(OUT, f"contact_{k}.jpg"), [(scenes[0][0], 0.0)] + [(fn, d-0.05) for fn, d in scenes])
    else:
        (scenes, ev), name = REELS[mode]
        print(build(os.path.join(OUT, mode), name, scenes, ev))
