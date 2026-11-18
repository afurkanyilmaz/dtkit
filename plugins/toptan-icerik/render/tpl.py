"""Shared brand template for week-1 Reels (frame-0-full, brand palette, small logo at end)."""
import sys, os, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from render import (W, H, FPS, BLACK, BOLD, SEMI, MED, BG, CARD, WHITE, CREAM, GREY, ICE, RED,
                    eo, eio, prog, text_layer, reveal, rrect, new_canvas, wordmark, kick, add, restaurant_card)

GOLD = ICE
DARKRED = (60, 22, 26)
SR = 48000

def mini_eu(c, cx, cy, w):
    h = w*2/3
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), radius=int(h*0.1), fill=R.EU_BLUE + (255,))
    for i in range(12):
        ang = -math.pi/2 + i*2*math.pi/12
        d.polygon(R._star(cx + h/3*math.cos(ang), cy + h/3*math.sin(ang), h/16), fill=R.EU_GOLD + (255,))
    c.alpha_composite(lay)

def top_label(c, txt="Avrupa'da döner toptancısı mısın?", y=370):
    f = SEMI(40); tw = f.getlength(txt); fw = 66; gap = 18
    x0 = W/2 - (fw + gap + tw)/2
    mini_eu(c, x0 + fw/2, y, fw)
    text_layer(c, txt, f, CREAM, x0 + fw + gap, y, 1.0, anchor="lm")

def line(c, x0, y, x1, col, w=8, p=1.0):
    if p <= 0: return
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line([(x0, y), (x0 + (x1-x0)*p, y)], fill=col + (255,), width=w)
    c.alpha_composite(lay)

def months_row(c, t, start, y=960, step=0.08):
    M = ["O", "Ş", "M", "N", "M", "H", "T", "A", "E", "E", "K", "A"]
    cw, gap = 66, 8; x0 = W/2 - (12*cw + 11*gap)/2
    for i, m in enumerate(M):
        q = eo(prog(t, start + i*step, 0.2)); x = x0 + i*(cw+gap)
        rrect(c, (x, y, x+cw, y+120), DARKRED, radius=12, alpha=q, outline=RED, width=3)
        text_layer(c, m, BOLD(36), WHITE, x+cw/2, y+60, q, anchor="mm")

def cta(c, t, l1, l2, word, word_size=150):
    wordmark(c, 330, alpha=eo(prog(t, 0.0, 0.3)), size=46)
    text_layer(c, l1, BOLD(66), WHITE, W//2, 470, 1.0)
    text_layer(c, l2, BOLD(66), WHITE, W//2, 560, 1.0)
    bp = eo(prog(t, 0.1, 0.35)); s = 0.9 + 0.1*bp
    bw, bh = 820*s, 220*s
    rrect(c, (W/2-bw/2, 860-bh/2, W/2+bw/2, 860+bh/2), CREAM, radius=36, alpha=bp)
    text_layer(c, word, BLACK(int(word_size*s)), BG, W//2, 860, bp, anchor="mm")
    text_layer(c, "Minimum sipariş 5 ton", SEMI(56), WHITE, W//2, 1040, 1.0)
    rrect(c, (150, 1170, 930, 1310), None, radius=30, alpha=1.0, outline=CREAM, width=5)
    text_layer(c, "donertrade.com", BLACK(84), CREAM, W//2, 1240, 1.0, anchor="mm")

# ---------- sound ----------
def tick(a=0.18, f=1800):
    k = int(0.035*SR); e = np.exp(-np.linspace(0, 9, k))
    return a*e*np.sin(2*np.pi*f*np.arange(k)/SR)
def pop(a=0.15):
    k = int(0.07*SR); tt = np.arange(k)/SR
    return a*np.exp(-tt*45)*np.sin(2*np.pi*(650+900*tt/0.07)*tt)
def low(a=0.18):
    k = int(0.25*SR); tt = np.arange(k)/SR
    return a*np.exp(-tt*10)*np.sin(2*np.pi*(180-120*tt/0.25)*tt)
def whoosh(d=0.8, a=0.25, seed=3):
    k = int(d*SR); x = np.convolve(np.random.default_rng(seed).uniform(-1, 1, k), np.ones(30)/30, mode="same")
    return a*3*x*np.sin(np.pi*np.linspace(0, 1, k))**2
def chime(a=0.12):
    k = int(1.2*SR); tt = np.arange(k)/SR
    return a*np.exp(-tt*2.5)*(np.sin(2*np.pi*220*tt)+0.6*np.sin(2*np.pi*330*tt))

def build(out_dir, name, scenes, events):
    """scenes: [(fn, dur)], events: [(scene_idx, offset, signal)]"""
    os.makedirs(out_dir, exist_ok=True)
    starts = [sum(d for _, d in scenes[:i]) for i in range(len(scenes))]
    for i, (fn, d) in enumerate(scenes):
        tmp = os.path.join(out_dir, f"tmp_s{i}.mp4"); final = os.path.join(out_dir, f"s{i}.mp4")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for f in range(int(round(d*FPS))): p.stdin.write(fn(f/FPS).convert("RGB").tobytes())
        p.stdin.close()
        if p.wait() != 0: sys.exit(f"scene {i} failed")
        os.replace(tmp, final)
    with open(os.path.join(out_dir, "list.txt"), "w") as f:
        for i in range(len(scenes)): f.write(f"file 's{i}.mp4'\n")
    total = sum(d for _, d in scenes); n = int(total*SR); t = np.arange(n)/SR
    bed = np.zeros(n); sfx = np.zeros(n)
    lfo = 0.6 + 0.4*np.sin(2*np.pi*0.25*t)
    bed += 0.05*lfo*(np.sin(2*np.pi*55*t) + 0.5*np.sin(2*np.pi*110*t) + 0.2*np.sin(2*np.pi*164.8*t))
    for st in np.arange(0.0, total-0.3, 0.5): add(bed, st, kick(0.28, 0.12))
    for si, off, sig in events: add(sfx, starts[si] + off, sig)
    mix = bed*0.9 + sfx*0.6
    fo = int(0.4*SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix/max(1e-9, np.abs(mix).max())*0.85
    wav = os.path.join(out_dir, "audio.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
    vo = os.path.join(out_dir, "video_only.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(out_dir, "list.txt"), "-c", "copy", vo], check=True)
    final = os.path.join(out_dir, name)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
    return final

def stills(out_path, shots):
    sheet = Image.new("RGB", (360*len(shots), 640))
    for i, (fn, tt) in enumerate(shots):
        sm = fn(tt).convert("RGB").resize((360, 640)); d = ImageDraw.Draw(sm)
        d.rectangle((0, 95, 359, 545), outline=(80, 200, 120))
        sheet.paste(sm, (i*360, 0))
    sheet.save(out_path, quality=88)
