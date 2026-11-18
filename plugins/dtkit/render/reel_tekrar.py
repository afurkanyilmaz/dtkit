import sys, os, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from render import (W, H, FPS, BLACK, BOLD, SEMI, MED, BG, CARD, WHITE, CREAM, GREY, ICE, RED,
                    eo, prog, text_layer, reveal, rrect, new_canvas, wordmark, kick, add)

GOLD = ICE
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "tekrar")
os.makedirs(OUT, exist_ok=True)

def mini_eu(c, cx, cy, w):
    h = w*2/3
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), radius=int(h*0.1), fill=R.EU_BLUE + (255,))
    for i in range(12):
        ang = -math.pi/2 + i*2*math.pi/12
        d.polygon(R._star(cx + h/3*math.cos(ang), cy + h/3*math.sin(ang), h/16), fill=R.EU_GOLD + (255,))
    c.alpha_composite(lay)

def top_label(c):
    f = SEMI(40); txt = "Avrupa'da döner toptancısı mısın?"
    tw = f.getlength(txt); fw = 66; gap = 18
    x0 = W/2 - (fw + gap + tw)/2
    mini_eu(c, x0 + fw/2, 370, fw)
    text_layer(c, txt, f, CREAM, x0 + fw + gap, 370, 1.0, anchor="lm")

def s1(t):  # hook — fully visible on frame 0
    c = new_canvas()
    top_label(c)
    z = 1.0 + 0.04*(1 - eo(prog(t, 0.0, 0.6)))
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    text_layer(lay, "Döner toptancısı", BLACK(104), WHITE, W//2, 520, 1.0)
    text_layer(lay, "fiyatla değil,", BLACK(104), GREY, W//2, 650, 1.0)
    text_layer(lay, "tekrar siparişle", BLACK(112), GOLD, W//2, 800, 1.0)
    text_layer(lay, "kazanır.", BLACK(112), WHITE, W//2, 935, 1.0)
    if z != 1.0:
        lay = lay.resize((int(W*z), int(H*z)), Image.BICUBIC)
        lay = lay.crop(((lay.width-W)//2, (lay.height-H)//2, (lay.width-W)//2 + W, (lay.height-H)//2 + H))
    c.alpha_composite(lay)
    up = eo(prog(t, 0.5, 0.5))
    if up > 0:
        d = Image.new("RGBA", c.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(d)
        dd.line([(W/2-390, 925), (W/2-390 + 780*up, 925)], fill=GOLD + (255,), width=8)
        c.alpha_composite(d)
    return c

def dot_grid(c, n_on, total=52, y0=760, cols=13, size=48, gap=16, col_on=GOLD):
    x0 = W/2 - (cols*size + (cols-1)*gap)/2
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(total):
        r, k = divmod(i, cols); x = x0 + k*(size+gap); y = y0 + r*(size+gap)
        on = i < n_on
        d.rounded_rectangle((x, y, x+size, y+size), radius=10,
                            fill=(col_on + (255,)) if on else (28, 30, 36, 255))
    c.alpha_composite(lay)

def s2(t):
    c = new_canvas()
    text_layer(c, "Ucuz fiyatla gelen müşteri:", BOLD(64), GREY, W//2, 470, 1.0)
    reveal(c, "1 sipariş.", BLACK(170), WHITE, 560, t, 0.15)
    dot_grid(c, 1 if t > 0.5 else 0, col_on=WHITE)
    reveal(c, "Sonra başka toptancı.", BOLD(62), RED, 1050, t, 1.4)
    return c

def s3(t):
    c = new_canvas()
    text_layer(c, "İyi dönerle kalan müşteri:", BOLD(64), GREY, W//2, 470, 1.0)
    n = int(round(52*eo(prog(t, 0.2, 1.6))))
    text_layer(c, f"{n} sipariş", BLACK(170), GOLD, W//2, 560, 1.0)
    dot_grid(c, n)
    reveal(c, "Her hafta. Bir yıl boyunca.", BOLD(62), WHITE, 1050, t, 1.9)
    return c

def s4(t):
    c = new_canvas()
    text_layer(c, "Kazandıran", BLACK(110), WHITE, W//2, 560, 1.0)
    text_layer(c, "ilk satış değil,", BLACK(110), GREY, W//2, 690, 1.0)
    reveal(c, "52. sipariş.", BLACK(150), GOLD, 850, t, 0.4)
    return c

def s5(t):  # CTA — logo small
    c = new_canvas(url=False)
    p = eo(prog(t, 0.0, 0.3))
    wordmark(c, 330, alpha=p, size=46)
    text_layer(c, "Düzenli tedarik teklifi", BOLD(66), WHITE, W//2, 470, 1.0)
    text_layer(c, "için DM'den yaz:", BOLD(66), WHITE, W//2, 560, 1.0)
    bp = eo(prog(t, 0.1, 0.35)); s = 0.9 + 0.1*bp
    bw, bh = 820*s, 220*s
    rrect(c, (W/2-bw/2, 860-bh/2, W/2+bw/2, 860+bh/2), CREAM, radius=36, alpha=bp)
    text_layer(c, "TEKRAR", BLACK(int(150*s)), BG, W//2, 860, bp, anchor="mm")
    text_layer(c, "Minimum sipariş 5 ton", SEMI(56), WHITE, W//2, 1040, 1.0)
    rrect(c, (150, 1170, 930, 1310), None, radius=30, alpha=1.0, outline=CREAM, width=5)
    text_layer(c, "donertrade.com", BLACK(84), CREAM, W//2, 1240, 1.0, anchor="mm")
    return c

SCENES = [(s1, 3.0), (s2, 2.9), (s3, 3.3), (s4, 2.2), (s5, 3.2)]
STARTS = [sum(d for _, d in SCENES[:i]) for i in range(len(SCENES))]
SR = 48000

def audio():
    total = sum(d for _, d in SCENES); n = int(total*SR); t = np.arange(n)/SR
    bed = np.zeros(n); sfx = np.zeros(n)
    lfo = 0.6 + 0.4*np.sin(2*np.pi*0.25*t)
    bed += 0.05*lfo*(np.sin(2*np.pi*55*t) + 0.5*np.sin(2*np.pi*110*t) + 0.2*np.sin(2*np.pi*164.8*t))
    for st in np.arange(0.0, total-0.3, 0.5): add(bed, st, kick(0.28, 0.12))
    def tick(a=0.18):
        k = int(0.035*SR); e = np.exp(-np.linspace(0, 9, k))
        return a*e*np.sin(2*np.pi*1800*np.arange(k)/SR)
    def pop(a=0.12):
        k = int(0.06*SR); tt = np.arange(k)/SR
        return a*np.exp(-tt*50)*np.sin(2*np.pi*(700+900*tt/0.06)*tt)
    S = STARTS
    add(sfx, S[0], kick(1.0, 0.5)); add(sfx, S[0]+0.5, tick())
    add(sfx, S[1], kick(0.7, 0.35)); add(sfx, S[1]+0.15, tick()); add(sfx, S[1]+0.5, pop(0.3))
    add(sfx, S[1]+1.4, kick(0.6, 0.3))
    add(sfx, S[2], kick(0.7, 0.35))
    prev = 0
    for f in range(int(2.0*FPS)):
        tt = 0.2 + f/FPS; k = int(round(52*eo(prog(tt, 0.2, 1.6))))
        if k > prev: add(sfx, S[2]+tt, pop()); prev = k
    add(sfx, S[2]+1.9, tick())
    add(sfx, S[3], tick()); add(sfx, S[3]+0.4, kick(0.9, 0.45))
    add(sfx, S[4], kick(1.0, 0.5))
    k = int(1.2*SR); tt = np.arange(k)/SR
    add(sfx, S[4]+0.2, 0.12*np.exp(-tt*2.5)*(np.sin(2*np.pi*220*tt)+0.6*np.sin(2*np.pi*330*tt)))
    mix = bed*0.9 + sfx*0.6
    fo = int(0.4*SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix/max(1e-9, np.abs(mix).max())*0.85
    with wave.open(os.path.join(OUT, "audio.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())

def render_scene(i, fn, dur):
    tmp = os.path.join(OUT, f"tmp_s{i}.mp4"); final = os.path.join(OUT, f"s{i}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(int(round(dur*FPS))): p.stdin.write(fn(f/FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, final)
    else: sys.exit(f"scene {i} failed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        ims = [fn(tt).convert("RGB") for fn, tt in [(s1, 0.0), (s2, 2.8), (s3, 3.2), (s4, 2.1), (s5, 3.0)]]
        ims[0].save(os.path.join(OUT, "frame0.jpg"), quality=90)
        sheet = Image.new("RGB", (1800, 640))
        for i, im in enumerate(ims):
            sm = im.resize((360, 640))
            d = ImageDraw.Draw(sm)  # mark 4:5 feed-crop safe zone
            d.rectangle((0, 285/3, 359, 1635/3), outline=(80, 200, 120))
            sheet.paste(sm, (i*360, 0))
        sheet.save(os.path.join(OUT, "contact.jpg"), quality=88)
    else:
        for i, (fn, d) in enumerate(SCENES): render_scene(i, fn, d)
        with open(os.path.join(OUT, "list.txt"), "w") as f:
            for i in range(len(SCENES)): f.write(f"file 's{i}.mp4'\n")
        audio()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"),
                        "-c", "copy", os.path.join(OUT, "video_only.mp4")], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(OUT, "video_only.mp4"), "-i", os.path.join(OUT, "audio.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        os.path.join(OUT, "DonerTrade_Video11_H73.mp4")], check=True)
        print("done")
