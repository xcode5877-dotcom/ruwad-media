"""Render the 'رسالة من ابنك' exam-period carousel for RUWAD as 1080x1350 PNGs."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "2026-10-25-risala-min-ibnak"
OUT.mkdir(parents=True, exist_ok=True)
FONTS = ROOT / "node_modules/@fontsource/rubik/files"

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

font_css = ""
for w in (400, 500, 700, 800):
    for sub in ("arabic", "latin"):
        f = FONTS / f"rubik-{sub}-{w}-normal.woff2"
        font_css += f"@font-face{{font-family:Rubik;font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"

LOGO_W = b64(ROOT / "logo-white.png")
LOGO_T = b64(ROOT / "logo-teal.png")

CSS = font_css + """
:root{--teal:#22524E;--teal-d:#163A37;--mint:#E3EEE9;--cream:#FBF7F0;--accent:#F0A04B;--ink:#1A2B29;--muted:#5E6E6B}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{font-family:Rubik,sans-serif;direction:rtl;color:var(--ink);overflow:hidden}
.slide{width:1080px;height:1350px;position:relative;padding:90px 90px}
.teal{background:var(--teal);color:#fff}
.cream{background:var(--cream)}
.logo{position:absolute;top:70px;right:90px;height:62px}
.pager{position:absolute;bottom:64px;left:90px;direction:ltr;font-size:30px;font-weight:500;opacity:.75}
.swipe{position:absolute;bottom:64px;right:90px;font-size:32px;font-weight:500}
/* cover */
.notif{margin-top:300px;background:#fff;color:var(--ink);border-radius:44px;padding:40px 44px;box-shadow:0 30px 70px rgba(0,0,0,.28);display:flex;gap:30px;align-items:flex-start}
.app{width:96px;height:96px;border-radius:26px;background:var(--accent);flex:none;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#fff}
.nt{display:flex;justify-content:space-between;font-size:32px;color:var(--muted);margin-bottom:10px}
.nt b{color:var(--ink);font-weight:700;font-size:36px}
.nb{font-size:40px;line-height:1.45;font-weight:500}
.h1{font-size:100px;font-weight:800;line-height:1.18;margin-top:110px}
.h1 em{font-style:normal;color:var(--accent)}
/* chat */
.chat{position:absolute;inset:0;background:#EFE7DB;display:flex;flex-direction:column}
.bar{background:var(--teal);color:#fff;padding:70px 70px 34px;display:flex;align-items:center;gap:28px}
.av{width:92px;height:92px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:800}
.bar b{font-size:42px;display:block}.bar span{font-size:30px;opacity:.85}
.msgs{flex:1;padding:50px 70px;display:flex;flex-direction:column;gap:24px}
.m{align-self:flex-end;background:#fff;border-radius:34px 34px 34px 10px;padding:26px 36px 18px;font-size:42px;line-height:1.4;max-width:820px;box-shadow:0 3px 0 rgba(0,0,0,.06)}
.m i{display:block;font-style:normal;font-size:24px;color:var(--muted);text-align:left;margin-top:6px}
.typing{align-self:flex-end;background:#fff;border-radius:34px;padding:22px 34px;font-size:40px;letter-spacing:6px;color:var(--muted)}
.note{background:var(--teal);color:#fff;margin:0 70px 70px;border-radius:36px;padding:38px 44px;font-size:36px;line-height:1.5}
.note b{color:var(--accent)}
/* tips */
.tips{display:flex;flex-direction:column;justify-content:center;padding-bottom:140px}
.label{align-self:flex-start;background:var(--mint);color:var(--teal);font-weight:700;font-size:36px;padding:16px 34px;border-radius:999px}
.tip{display:flex;gap:44px;margin-top:100px;align-items:flex-start}
.num{flex:none;width:140px;height:140px;border-radius:50%;background:var(--teal);color:#fff;font-size:68px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tip h2{font-size:68px;font-weight:800;line-height:1.25;color:var(--teal);margin-top:8px}
.tip p{font-size:46px;line-height:1.55;margin-top:18px;color:var(--ink)}
.closing{margin-top:120px;border-top:6px solid var(--accent);padding-top:50px;font-size:72px;font-weight:800;line-height:1.3;color:var(--teal)}
/* cta */
.biglogo{display:block;height:170px;margin:170px auto 0}
.q{text-align:center;font-size:74px;font-weight:800;margin-top:110px;line-height:1.25}
.sub{text-align:center;font-size:42px;line-height:1.55;margin-top:36px;opacity:.95}
.wa{margin:80px auto 0;background:#fff;color:var(--teal);border-radius:999px;width:820px;padding:36px 0;text-align:center}
.wa small{display:block;font-size:30px;font-weight:500;color:var(--muted)}
.wa b{font-size:72px;font-weight:800;direction:ltr;display:block;letter-spacing:2px}
.place{text-align:center;font-size:34px;margin-top:50px;opacity:.85}
"""

def page(body, cls):
    return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='slide {cls}'>{body}</div></body></html>"

LW = f"<img class='logo' src='data:image/png;base64,{LOGO_W}'>"
LT = f"<img class='logo' src='data:image/png;base64,{LOGO_T}'>"
def pager(n): return f"<div class='pager'>{n} / 6</div>"

slides = []
# 1 cover
slides.append(page(LW + """
<div class='notif'><div class='app'>ا</div><div style='flex:1'>
<div class='nt'><b>ابني</b><span>الآن</span></div>
<div class='nb'>يمّا… بدي أحكيلك إشي، بس لا تعصّبي</div></div></div>
<div class='h1'>الرسالة اللي ابنك<br>ما رح يبعتها<br><em>بفترة الامتحانات</em></div>
<div class='swipe'>اقرأوها للآخر ←</div>""" + pager(1), "teal"))
# 2 chat
slides.append(page("""<div class='chat'>
<div class='bar'><div class='av'>ا</div><div><b>ابني</b><span>متصل الآن</span></div></div>
<div class='msgs'>
<div class='m'>يمّا عندي امتحان بكرا<i>21:04</i></div>
<div class='m'>بقعد أدرس… وبعد خمس دقايق بلاقي حالي عالتلفون<i>21:04</i></div>
<div class='m'>مش قصدي والله، بدي أنجح<i>21:05</i></div>
<div class='m'>بس راسي مليان ضجة<i>21:05</i></div>
<div class='m'>ساعدوني… بس بدون صريخ<i>21:06</i></div>
</div>
<div class='note'>كثير ولاد بحسّوا هيك بعد سنين الكورونا والحرب.<br><b>المشكلة مش إنهم ما بدهم يدرسوا.</b></div>
</div>""", "cream"))
# 3 tips 1-2
slides.append(page(LT + """<span class='label'>5 أشياء بتفرق الليلة</span>
<div class='tip'><div class='num'>1</div><div><h2>التلفون برّا الغرفة</h2><p>مش مقلوب على الطاولة. حتى وهو ساكت، بيضل يشدّ انتباهه.</p></div></div>
<div class='tip'><div class='num'>2</div><div><h2>25 دقيقة دراسة،<br>5 دقايق راحة</h2><p>والراحة بعيد عن الشاشة: كاسة مَي، مشوار بالبيت، إشي ياكله.</p></div></div>
""" + pager(3), "cream tips"))
# 4 tips 3-4
slides.append(page(LT + """<span class='label'>5 أشياء بتفرق الليلة</span>
<div class='tip'><div class='num'>3</div><div><h2>غيّروا السؤال</h2><p>بدل «درست؟» اسألوه «شو أصعب سؤال لهلأ؟». الأول بيسكّر الحديث، والثاني بيفتحه.</p></div></div>
<div class='tip'><div class='num'>4</div><div><h2>النوم جزء من الدراسة</h2><p>نوم بكّير قبل الامتحان بيفيده أكثر من ساعة حفظ زيادة بآخر الليل.</p></div></div>
""" + pager(4), "cream tips"))
# 5 tip 5 + closing
slides.append(page(LT + """<span class='label'>5 أشياء بتفرق الليلة</span>
<div class='tip'><div class='num'>5</div><div><h2>إذا علق، مش وقت عصبية</h2><p>اقعدوا جنبه عشر دقايق. وإذا المادة صعبة عليكم كمان، دوّروا مع بعض على مين يشرحله.</p></div></div>
<div class='closing'>التلفون مش العدو.<br>بس الليلة مش وقته.</div>
""" + pager(5), "cream tips"))
# 6 CTA
slides.append(page(f"""<img class='biglogo' src='data:image/png;base64,{LOGO_W}'>
<div class='q'>علق بمادة<br>قبل الامتحان؟</div>
<div class='sub'>دروس قبل الامتحان بحجز مسبق<br>فردي وجماعي، لكل الصفوف</div>
<div class='wa'><small>احجزوا على واتساب</small><b>054-6111668</b></div>
<div class='place'>معهد رُوّاد · دبورية</div>""" + pager(6), "teal"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(slides, 1):
        pg.set_content(html, wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(OUT / f"slide-{i}.png"))
    b.close()
print(OUT)
