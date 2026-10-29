"""Countdown campaign stories (العدّاد اشتغل), 1080x1920 PNG.
Run from a folder holding Rubik woff2 files (rubik-{arabic,latin}-{500,700,800,900}-normal.woff2), logo-white.png and cov-countdown.jpg.
Safe zones: top 250px, bottom 330px kept clear of key content."""
import base64, json, pathlib, sys
from playwright.sync_api import sync_playwright

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'out'); OUT.mkdir(parents=True, exist_ok=True)
def b64(p): return base64.b64encode((SRC / p).read_bytes()).decode()
fonts = ''
for w in (500, 700, 800, 900):
    for sub, fam in (('arabic', 'R'), ('latin', 'L')):
        fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f'rubik-{sub}-{w}-normal.woff2')})}}\n"

CSS = fonts + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:R,L;direction:rtl;color:#fff}
.s{width:1080px;height:1920px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 42%,#2B5E59 0,#163A37 48%,#0B201E 100%)}
.s::before{content:"";position:absolute;inset:-100px;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:120px 120px;transform:rotate(-8deg)}
.glow{position:absolute;width:1300px;height:1300px;left:-110px;top:320px;border-radius:50%;background:radial-gradient(circle,rgba(255,216,77,.22) 0,rgba(255,216,77,0) 60%)}
.logo{position:absolute;top:270px;right:90px;height:70px}
.tag{position:absolute;top:290px;left:90px;font-family:L;font-weight:700;font-size:30px;letter-spacing:7px;color:#FFD84D;direction:ltr}
.c{position:absolute;left:0;right:0;text-align:center}
.num{font-family:L;font-weight:900;direction:ltr;letter-spacing:-5px;line-height:1}
.chip{display:inline-block;font-weight:800;border-radius:999px;padding:14px 44px}
.card{position:absolute;left:90px;right:90px;height:220px;border-radius:40px;background:#fff;color:#14332F;display:flex;align-items:center;padding:0 46px;gap:34px;box-shadow:0 20px 0 rgba(0,0,0,.25)}
.card .g{flex:none;width:150px;height:150px;border-radius:30px;background:#22524E;color:#FFD84D;display:flex;align-items:center;justify-content:center;flex-direction:column;font-weight:900;font-size:60px;line-height:1}
.card .g small{font-size:27px;color:#fff;font-weight:700;margin-top:8px}
.card b{display:block;font-size:54px;font-weight:900;line-height:1.15}
.card span{display:block;font-size:40px;font-weight:700;color:#E2574C;margin-top:6px}
.tip{position:absolute;left:110px;right:110px;background:#FFD84D;color:#14332F;border-radius:30px;padding:34px 40px;font-size:48px;font-weight:800;line-height:1.45;text-align:center;transform:rotate(-1.5deg);box-shadow:0 14px 30px rgba(0,0,0,.3)}
.reply{position:absolute;bottom:360px;left:120px;right:120px;text-align:center;border:4px solid rgba(255,255,255,.7);border-radius:999px;padding:22px 0;font-size:44px;font-weight:700}
"""
LOGO = f"<img class='logo' src='data:image/png;base64,{b64('logo-white.png')}'>"
TAG = "<div class='tag'>THE COUNTDOWN IS ON</div>"
def page(body): return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='s'><div class='glow'></div>{LOGO}{TAG}{body}</div></body></html>"

def card(top, g, gname, what, when):
    return f"<div class='card' style='top:{top}px'><div class='g'>{g}<small>{gname}</small></div><div><b>{what}</b><span>{when}</span></div></div>"

def new_reel():
    return page(f"<div class='c' style='top:430px'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:56px'>ريل جديد</span></div>"
                f"<img src='data:image/jpeg;base64,{b64('cov-countdown.jpg')}' style='position:absolute;top:570px;left:50%;width:470px;margin-left:-235px;border-radius:34px;border:10px solid #fff;transform:rotate(-3deg);box-shadow:0 30px 60px rgba(0,0,0,.45)'>"
                "<div class='c' style='bottom:400px;font-size:62px;font-weight:900'>أول امتحان مش 26/11 ↑</div>")

def tomorrow(cards, foot):
    return page("<div class='c' style='top:420px;font-size:70px;font-weight:800'>العدّاد بيقول</div>"
                "<div class='c' style='top:510px;font-size:250px;font-weight:900;color:#FFD84D;line-height:1.1'>بكرة</div>"
                + cards + f"<div class='reply'>{foot}</div>")

def luck(title, cards, tip):
    return page(f"<div class='c' style='top:420px;font-size:56px;font-weight:700;opacity:.9'>صباح الخير يا أبطال ☀️</div>"
                f"<div class='c' style='top:500px;font-size:132px;font-weight:900;color:#FFD84D;line-height:1.15'>{title}</div>"
                + cards + f"<div class='tip' style='top:1230px'>{tip}</div>")

STORIES = [
    ("2026-10-30T21:30", "cd-new-reel", new_reel()),
    ("2026-10-31T21:00", "cd-tomorrow-8-9", tomorrow(
        card(820, 8, 'الثامن', 'مهمة رياضيات محوسبة', 'الأحد 1/11') + card(1080, 9, 'التاسع', 'امتحان لغة عربية', 'الأحد 1/11'),
        'نوم بكّير الليلة 😴 · ردّوا بـ 💚 للأبطال')),
    ("2026-11-01T07:15", "cd-luck-8-9", luck('بالتوفيق اليوم',
        card(760, 8, 'الثامن', 'مهمة رياضيات محوسبة', 'اليوم') + card(1010, 9, 'التاسع', 'امتحان لغة عربية', 'اليوم'),
        'اقرأ السؤال مرّتين قبل ما تجاوب.<br>والسؤال الصعب؟ اتركه للآخر.')),
    ("2026-11-02T07:15", "cd-luck-8", luck('بالتوفيق يا ثامن',
        card(820, 8, 'الثامن', 'مهمة رياضيات محوسبة', 'اليوم كمان'),
        'بالمهمة المحوسبة: افحص الجواب<br>قبل ما تكبس «التالي» 👀')),
    ("2026-11-02T21:30", "cd-tomorrow-7", tomorrow(
        card(860, 7, 'السابع', 'مهمة رياضيات محوسبة', 'الثلاثاء 3/11'),
        'السابع جاهز؟ ردّوا بـ 💪')),
    ("2026-11-03T07:15", "cd-luck-7", luck('بالتوفيق يا سابع',
        card(820, 7, 'السابع', 'مهمة رياضيات محوسبة', 'اليوم'),
        'اكتب الخطوات على ورقة جنبك،<br>حتى لو المهمة على الحاسوب.')),
    ("2026-11-04T07:15", "cd-luck-7-b", luck('السابع، كمّلوا!',
        card(820, 7, 'السابع', 'مهمة رياضيات محوسبة', 'اليوم كمان'),
        'ما تستعجل بالأول،<br>الوقت بيكفي إذا مشيت سؤال سؤال.')),
    ("2026-11-04T21:30", "cd-tomorrow-7-exam", tomorrow(
        card(860, 7, 'السابع', 'امتحان رياضيات', 'الخميس 5/11')
        + "<div class='c' style='top:1150px'><span class='chip' style='background:#E2574C;font-size:46px'>والفصلي بعد 22 يوم ⏱</span></div>",
        'مراجعة أخيرة الليلة · <bdi dir=ltr>054-6111668</bdi>')),
    ("2026-11-05T07:15", "cd-luck-7-exam", luck('بالتوفيق يا سابع',
        card(820, 7, 'السابع', 'امتحان رياضيات', 'اليوم'),
        'جاوب السهل أول، وارجع للصعب.<br>إحنا فخورين فيك قبل العلامة 💚')),
]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for when, slug, html in STORIES:
            pg.set_content(html, wait_until='load'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / f'{when[:10]}-{slug}.png'))
        b.close()
    json.dump([[w, f'{w[:10]}-{s}.png'] for w, s, _ in STORIES], open(OUT / 'schedule.json', 'w'))
    print(len(STORIES))
