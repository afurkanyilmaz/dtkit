# dtkit

Claude için açık kaynak bir skill ve eklenti deposu: Avrupa'daki gurbetçi döner toptancılarına yönelik Türkçe B2B Instagram, TikTok ve Facebook içeriği üretir (hook, Reels videosu, carousel, Story, açıklama, haftalık takvim). İlk marka profili: [DonerTrade](https://donertrade.com).

## Kurulum

### Claude Code (her bilgisayarda)
```bash
claude plugin marketplace add afurkanyilmaz/dtkit
claude plugin install dtkit@dtkit
```
Oturum içinde: `/dtkit:icerik`

### claude.ai (web, masaüstü, mobil)
`plugins/dtkit/skills/icerik/SKILL.md` dosyasını Settings > Capabilities > Skills bölümünden yükleyin ya da Claude'a "bu skill'i kaydet" deyin.

## İçerik

| Yol | Ne |
| --- | --- |
| `plugins/dtkit/skills/icerik/SKILL.md` | Kurallar, hedef kitle, marka, video şablonu, paylaşım ve DM yöntemi |
| `plugins/dtkit/render/` | Reels (1080×1920), carousel (1080×1350) ve Story üreten Python + FFmpeg kodu |
| `plugins/dtkit/brand/` | DonerTrade logosu (şeffaf PNG) |
| `plugins/dtkit/docs/` | Proje arşiv notu ve 1. hafta takvimi |

## Video üretimi
```bash
pip install pillow numpy
export INTER_FONT_DIR=/path/to/inter/fonts/
cd plugins/dtkit/render
python3 reels.py stills   # önizleme
python3 reels.py R1       # tek Reels
python3 static.py         # carousel + Story
```

## Lisans
Kod ve dokümanlar MIT. Logo DonerTrade'e aittir, markanın izni olmadan başka projede kullanılamaz. Inter fontu OFL-1.1 lisanslıdır ve depoya dahil değildir.
