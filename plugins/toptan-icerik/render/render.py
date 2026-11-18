import sys, os, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(OUT, "..", "brand")
FONT_DIR = os.environ.get("INTER_FONT_DIR", "/usr/share/fonts/opentype/inter/")
FD = FONT_DIR if FONT_DIR.endswith("/") else FONT_DIR + "/"
def F(name, size): return ImageFont.truetype(FD + name, size)
BLACK = lambda s: F("InterDisplay-Black.otf", s)
BOLD = lambda s: F("InterDisplay-Bold.otf", s)
SEMI = lambda s: F("Inter-SemiBold.otf", s)
MED = lambda s: F("Inter-Medium.otf", s)

BG = (7, 9, 13)
CARD = (27, 29, 34)
WHITE = (242, 241, 237)
CREAM = WHITE
GREY = (140, 145, 155)
ICE = (226, 165, 76)  # döner altını (vurgu)
CHICKEN = (232, 184, 98)
BEEF = (122, 40, 34)
RED = (235, 72, 77)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x):  # ease out cubic
    x = clamp(x); return 1 - (1 - x) ** 3
def eio(x):
    x = clamp(x); return 4*x*x*x if x < .5 else 1 - (-2*x+2)**3/2
def prog(t, start, dur): return clamp((t - start) / dur)

# ---------- background ----------
def make_bg():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 90):
        d.line([(x, 0), (x, H)], fill=(15, 17, 22), width=1)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=(15, 17, 22), width=1)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W/2)/(W*0.75))**2 + ((yy - H/2)/(H*0.7))**2)
    v = clamp_arr = np.clip(1 - 0.55*np.clip(r - 0.35, 0, 1), 0.3, 1)
    a = np.asarray(img).astype(np.float32) * v[..., None]
    return Image.fromarray(a.astype(np.uint8))
BGIMG = make_bg()

# ---------- drawing helpers ----------
def text_layer(canvas, txt, font, color, cx, y, alpha=1.0, dy=0, anchor="mt"):
    if alpha <= 0: return
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((cx, y + dy), txt, font=font, fill=color + (int(255*alpha),), anchor=anchor)
    canvas.alpha_composite(lay)

def reveal(canvas, txt, font, color, y, t, start, cx=W//2, anchor="mt"):
    p = eo(prog(t, start, 0.35))
    text_layer(canvas, txt, font, color, cx, y, alpha=p, dy=(1-p)*28, anchor=anchor)

def rrect(canvas, box, fill, radius=28, alpha=1.0, outline=None, width=3):
    if alpha <= 0: return
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = fill + (int(255*alpha),) if fill else None
    o = outline + (int(255*alpha),) if outline else None
    d.rounded_rectangle(box, radius=radius, fill=f, outline=o, width=width)
    canvas.alpha_composite(lay)

def new_canvas(url=True):
    c = BGIMG.convert("RGBA")
    if url: text_layer(c, "donertrade.com", BOLD(46), CREAM, W//2, 1480, 0.9)
    return c

_LOGO = {}
def _logo(name):
    if name not in _LOGO:
        im = Image.open(os.path.join(BRAND, f"logo_{name}.png")).convert("RGBA")
        _LOGO[name] = im.crop(im.getbbox())
    return _LOGO[name]

def _paste_logo(c, name, y, alpha, height, cx=W//2):
    if alpha <= 0: return
    im = _logo(name); w = int(im.width * height / im.height)
    im = im.resize((w, int(height)), Image.LANCZOS)
    a = im.split()[3].point(lambda v: int(v*alpha)); im.putalpha(a)
    c.alpha_composite(im, (int(cx - w/2), int(y)))

def wordmark(c, y, alpha=1.0, size=58, cx=W//2):
    _paste_logo(c, "word", y, alpha, size*1.05, cx)

def logo_full(c, y, alpha=1.0, height=250, cx=W//2):
    _paste_logo(c, "full", y, alpha, height, cx)

def restaurant_card(c, x, y, name, kg, alpha=1.0, tint=None, w=860, h=130):
    fill = CARD if tint is None else tint
    rrect(c, (x, y, x+w, y+h), fill, radius=24, alpha=alpha)
    text_layer(c, name, SEMI(46), WHITE, x+44, y+h/2, alpha, anchor="lm")
    text_layer(c, kg, BOLD(46), ICE if tint is None else WHITE, x+w-44, y+h/2, alpha, anchor="rm")

# ---------- scenes ----------
EU_BLUE = (0, 51, 153); EU_GOLD = (255, 204, 0)
def _star(cx, cy, R):
    r = R*0.382; pts = []
    for k in range(10):
        ang = -math.pi/2 + k*math.pi/5; rad = R if k % 2 == 0 else r
        pts.append((cx + rad*math.cos(ang), cy + rad*math.sin(ang)))
    return pts

def scene0(t):
    c = new_canvas()
    fw = 600; fh = fw*2/3; cx, cy = W/2, 560
    p = eo(prog(t, 0.0, 0.35))
    if p > 0:
        s_ = 0.85 + 0.15*p; w, h = fw*s_, fh*s_
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), radius=int(h*0.06), fill=EU_BLUE + (int(255*p),))
        for i in range(12):
            q = eo(prog(t, 0.25 + i*0.05, 0.2))
            if q <= 0: continue
            ang = -math.pi/2 + i*2*math.pi/12
            d.polygon(_star(cx + h/3*math.cos(ang), cy + h/3*math.sin(ang), h/18*(0.5+0.5*q)), fill=EU_GOLD + (int(255*q),))
        c.alpha_composite(lay)
    reveal(c, "Avrupa'da", BLACK(110), WHITE, 860, t, 0.55)
    reveal(c, "döner toptancısı", BLACK(118), ICE, 990, t, 0.7)
    reveal(c, "mısın?", BLACK(110), WHITE, 1130, t, 0.85)
    return c

def scene1(t):  # hook
    c = new_canvas()
    reveal(c, "Ucuz döner alan", BLACK(104), WHITE, 300, t, 0.00)
    reveal(c, "toptancı,", BLACK(104), WHITE, 420, t, 0.20)
    reveal(c, "pahalı müşteri", BLACK(104), RED, 560, t, 0.55)
    reveal(c, "kaybeder.", BLACK(104), RED, 680, t, 0.75)
    names = [("Restoran A", "400 kg/hafta"), ("Restoran B", "350 kg/hafta"),
             ("Restoran C", "400 kg/hafta"), ("Restoran D", "450 kg/hafta")]
    for i, (n, k) in enumerate(names):
        p = eo(prog(t, 0.15 + i*0.08, 0.4))
        y = 850 + i*145 + (1-p)*40
        strike = prog(t, 1.55, 0.3) if i == 2 else 0
        a = p * (1 - 0.55*strike)
        restaurant_card(c, 110, y, n, k, alpha=a)
        if i == 2 and strike > 0:
            lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.line([(90, y+65), (90 + eo(strike)*900, y+65)], fill=RED + (255,), width=12)
            c.alpha_composite(lay)
    return c

def scene2(t):  # 4.5 s
    c = new_canvas()
    reveal(c, "Kilo başı 20 sent", BOLD(64), GREY, 300, t, 0.0)
    v = 0.20 * eo(prog(t, 0.2, 1.0))
    reveal(c, f"+{v:.2f} €/kg".replace(".", ","), BLACK(170), ICE, 400, t, 0.1)
    reveal(c, "kazanırsın.", BOLD(64), GREY, 600, t, 0.5)
    reveal(c, "Restoran tek kötü partide", BOLD(70), WHITE, 830, t, 2.0)
    reveal(c, "başka toptancıya geçer.", BOLD(70), RED, 920, t, 2.4)
    p_in = eo(prog(t, 0.6, 0.4))
    out = eio(prog(t, 3.0, 1.0))
    x = 110 + out * 1100
    tint = tuple(int(CARD[i] + (RED[i]*0.55 - CARD[i]) * prog(t, 2.6, 0.4)) for i in range(3))
    restaurant_card(c, x, 1180, "Restoran C", "400 kg/hafta", alpha=p_in, tint=tint)
    if out > 0.02:
        a = clamp(1 - out*1.2)
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        ax = 110 + out*500
        d.line([(110, 1390), (ax, 1390)], fill=RED + (int(255*a),), width=8)
        d.polygon([(ax, 1370), (ax+36, 1390), (ax, 1410)], fill=RED + (int(255*a),))
        c.alpha_composite(lay)
    return c

def scene3(t):  # 5 s
    c = new_canvas()
    reveal(c, "Bir restoran", BLACK(96), WHITE, 290, t, 0.0)
    reveal(c, "ne kadar döner alır?", BLACK(80), WHITE, 410, t, 0.2)
    rows_y = 640
    reveal(c, "400 kg / hafta", BOLD(96), WHITE, rows_y, t, 0.5)
    reveal(c, "× 52 hafta", BOLD(96), GREY, rows_y + 140, t, 1.1)
    lp = eo(prog(t, 1.2, 0.3))
    if lp > 0:
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.line([(W/2 - 330*lp, rows_y + 290), (W/2 + 330*lp, rows_y + 290)], fill=GREY + (255,), width=5)
        c.alpha_composite(lay)
    kg = int(round(20800 * eo(prog(t, 1.3, 1.0))))
    reveal(c, f"= {kg:,} kg".replace(",", "."), BLACK(120), WHITE, rows_y + 330, t, 1.3)
    reveal(c, "≈ 21 ton / yıl", BLACK(140), RED, rows_y + 520, t, 2.4)
    reveal(c, "örnek hesap", MED(40), GREY, 1370, t, 2.6)
    return c

def scene4(t):  # 4 s
    c = new_canvas()
    p = eo(prog(t, 0.0, 0.4))
    # two boxes: small gain vs big loss
    rrect(c, (110, 300 + (1-p)*30, 520, 560 + (1-p)*30), CARD, alpha=p)
    text_layer(c, "+0,20 €/kg", BOLD(58), ICE, 315, 380 + (1-p)*30, p)
    text_layer(c, "kazanç", MED(42), GREY, 315, 470 + (1-p)*30, p)
    p2 = eo(prog(t, 0.3, 0.4))
    rrect(c, (560, 300 + (1-p2)*30, 970, 560 + (1-p2)*30), (60, 22, 26), alpha=p2, outline=RED, width=4)
    text_layer(c, "21 ton/yıl", BOLD(58), RED, 765, 380 + (1-p2)*30, p2)
    text_layer(c, "kayıp", MED(42), GREY, 765, 470 + (1-p2)*30, p2)
    reveal(c, "Ucuz parti değil,", BLACK(92), WHITE, 760, t, 1.2)
    reveal(c, "restoranını", BLACK(92), ICE, 880, t, 1.5)
    reveal(c, "tutan döner.", BLACK(92), ICE, 1000, t, 1.7)
    wp = eo(prog(t, 2.5, 0.5))
    logo_full(c, 1110 + (1-wp)*24, alpha=wp, height=300)
    return c

def scene5(t):  # 3 s  CTA
    c = new_canvas(url=False)
    p = eo(prog(t, 0.0, 0.4))
    wordmark(c, 300, alpha=p, size=80)
    reveal(c, "Numune ve teklif için", BOLD(64), WHITE, 520, t, 0.15)
    reveal(c, "DM'den yaz:", BOLD(64), WHITE, 605, t, 0.3)
    bp = eo(prog(t, 0.45, 0.45))
    s = 0.85 + 0.15*bp
    bw, bh = 820*s, 220*s
    rrect(c, (W/2-bw/2, 800-bh/2+110, W/2+bw/2, 800+bh/2+110), CREAM, radius=36, alpha=bp)
    text_layer(c, "TEKLİF", BLACK(int(140*s)), BG, W//2, 910, bp, anchor="mm")
    reveal(c, "Minimum sipariş 5 ton", SEMI(56), WHITE, 1100, t, 0.8)
    up = eo(prog(t, 1.0, 0.35))
    rrect(c, (150, 1240+(1-up)*20, 930, 1380+(1-up)*20), None, radius=30, alpha=up, outline=CREAM, width=5)
    text_layer(c, "donertrade.com", BLACK(84), CREAM, W//2, 1310+(1-up)*20, up, anchor="mm")
    return c

import json as _json
TEMPO = 1.17
try:
    VO = _json.load(open(os.path.join(OUT, "..", "voice", "info.json")))["durs"]
except Exception:
    VO = [1.9, 3.4, 5.6, 4.5, 3.8, 4.6]  # Harrison VO line lengths (s)
PADS = [0.15, 0.2, 0.25, 0.25, 0.25, 0.6]
DURS = [round(v/TEMPO + p, 2) for v, p in zip(VO, PADS)]
SCENES = list(zip([scene0, scene1, scene2, scene3, scene4, scene5], DURS))
STARTS = [sum(DURS[:i]) for i in range(len(DURS))]

def render_scene(i, fn, dur):
    tmp = os.path.join(OUT, f"tmp_s{i}.mp4"); final = os.path.join(OUT, f"s{i}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for f in range(n):
        p.stdin.write(fn(f / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, final)
    else: sys.exit(f"scene {i} failed")

# ---------- audio ----------
SR = 48000
def load_vo(i):
    import soundfile as sf
    tmp = f"/tmp/vo{i}.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",fos.path.join(OUT, "..", "voice", f"line{i}.wav"),
                    "-af",f"atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80",
                    "-ar",str(SR),"-ac","1",tmp], check=True)
    x, _ = sf.read(tmp, dtype="float64"); return x

def audio():
    total = sum(DURS)
    n = int(total * SR); t = np.arange(n) / SR
    bed = np.zeros(n); sfx = np.zeros(n); vo = np.zeros(n)
    lfo = 0.6 + 0.4*np.sin(2*np.pi*0.25*t)
    bed += 0.05*lfo*(np.sin(2*np.pi*55*t) + 0.5*np.sin(2*np.pi*110*t) + 0.2*np.sin(2*np.pi*164.8*t))
    for st in np.arange(0.0, total-0.3, 0.6): add(bed, st, kick(0.25, 0.12))
    rng = np.random.default_rng(1)
    def tick(a=0.18):
        k = int(0.035*SR); e = np.exp(-np.linspace(0, 9, k))
        return a*e*np.sin(2*np.pi*1800*np.arange(k)/SR)
    def strike(a=0.5):
        k = int(0.18*SR); e = np.exp(-np.linspace(0, 6, k)); return a*e*rng.uniform(-1, 1, k)
    def whoosh(d=0.9, a=0.25):
        k = int(d*SR); x = np.convolve(rng.uniform(-1, 1, k), np.ones(30)/30, mode="same")
        return a*3*x*np.sin(np.pi*np.linspace(0, 1, k))**2
    S = STARTS
    add(sfx, S[0], kick(0.9, 0.4))
    for o in [0.0, 0.15, 0.3, 0.5]: add(sfx, S[0]+o, tick())
    for o in [0.6+i*0.07 for i in range(6)]: add(sfx, S[0]+o, tick(0.08))
    add(sfx, S[1], kick(0.7, 0.35))
    for o in [0.0, 0.2, 0.55, 0.75]: add(sfx, S[1]+o, tick())
    add(sfx, S[1]+1.55, strike()); add(sfx, S[1]+1.55, kick(0.6, 0.3))
    for o in np.arange(0.2, 1.2, 0.08): add(sfx, S[2]+o, tick(0.1))
    add(sfx, S[2]+3.0, whoosh())
    for o in [0.5, 1.1]: add(sfx, S[3]+o, tick())
    for o in np.arange(1.3, 2.3, 0.07): add(sfx, S[3]+o, tick(0.08))
    add(sfx, S[3]+2.4, kick(0.9, 0.45))
    for o in [0.0, 0.3, 1.2, 1.5, 1.7]: add(sfx, S[4]+o, tick())
    add(sfx, S[4]+2.5, kick(0.8, 0.4))
    add(sfx, S[5], kick(1.0, 0.5))
    k = int(1.2*SR); tt = np.arange(k)/SR
    add(sfx, S[5]+0.45, 0.12*np.exp(-tt*2.5)*(np.sin(2*np.pi*220*tt)+0.6*np.sin(2*np.pi*330*tt)))
    for i in range(6):
        add(vo, S[i] + (0.05 if i else 0.0), load_vo(i))
    # duck bed + sfx under voice
    env = np.convolve(np.abs(vo), np.ones(int(0.15*SR))/int(0.15*SR), mode="same")
    duck = 1 - 0.55*np.clip(env/ (env.max()*0.3 + 1e-9), 0, 1)
    mix = 0.9*vo/ (np.abs(vo).max()+1e-9) + (bed*0.8 + sfx*0.45)*duck
    fo = int(0.5*SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix / max(1e-9, np.abs(mix).max()) * 0.89
    with wave.open(os.path.join(OUT, "audio.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())

def kick(a, d):
    k = int(d*SR); tt = np.arange(k)/SR
    f = 50 + 70*np.exp(-tt*30)
    ph = 2*np.pi*np.cumsum(f)/SR
    return a*np.exp(-tt*(6/d))*np.sin(ph)

def add(buf, start, sig):
    i = int(start*SR); j = min(len(buf), i+len(sig))
    if i < len(buf): buf[i:j] += sig[:j-i]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "stills":
        for i, (fn, t) in enumerate([(scene0, 1.8), (scene1, 2.4), (scene2, 3.6), (scene3, 3.4), (scene4, 3.4), (scene5, 2.5)]):
            fn(t).convert("RGB").save(os.path.join(OUT, f"still{i+1}.jpg"), quality=88)
    else:
        for i, (fn, d) in enumerate(SCENES): render_scene(i, fn, d)
        with open(os.path.join(OUT, "list.txt"), "w") as f:
            for i in range(len(SCENES)): f.write(f"file 's{i}.mp4'\n")
        audio()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"),
                        "-c", "copy", os.path.join(OUT, "video_only.mp4")], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(OUT, "video_only.mp4"), "-i", os.path.join(OUT, "audio.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        os.path.join(OUT, "DonerTrade_Video4_H62_marka.mp4")], check=True)
        print("done")
