"""Carousel 7/11: three-week exam plan for parents (1080x1350). Run: python3 build_plan_carousel.py <fonts+logo dir> <out dir>"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
def b64(p): return base64.b64encode((SRC / p).read_bytes()).decode()
F = ''
for w in (500, 700, 800, 900):
    F += f"@font-face{{font-family:R;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'rubik-arabic-{w}-normal.woff2')})}}\n"
    F += f"@font-face{{font-family:L;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'rubik-latin-{w}-normal.woff2')})}}\n"
for w in (500, 700):
    F += f"@font-face{{font-family:H;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'marhey-arabic-{w}-normal.woff2')})}}\n"
CSS = F + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:R,L;direction:rtl;color:#1D2B3A}
.s{width:1080px;height:1350px;position:relative;overflow:hidden}
.paper{background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px),#CFE0EE calc(100% - 3px));background-size:100% 72px;background-position:0 36px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:150px;width:4px;background:#F2A7A7;opacity:.8}
.hole{position:absolute;right:52px;width:44px;height:44px;border-radius:50%;background:#E6E1D6;box-shadow:inset 0 3px 6px rgba(0,0,0,.12)}
.teal{background:radial-gradient(circle at 50% 42%,#2B5E59 0,#163A37 55%,#0B201E 100%);color:#fff}
.hand{font-family:H}
.num{position:absolute;bottom:52px;left:70px;font-family:L;font-weight:700;font-size:34px;color:#7E8FB8}
.wk{display:inline-block;background:#22524E;color:#FFD84D;font-weight:900;font-size:40px;border-radius:999px;padding:10px 34px}
.date{display:inline-block;margin-right:16px;font-family:L;font-weight:700;font-size:36px;color:#E2574C;direction:ltr}
.title{font-family:H;font-weight:700;font-size:84px;white-space:nowrap;line-height:1.2;color:#1D2B3A;margin-top:26px}
.sticky{position:absolute;left:110px;right:200px;padding:44px 52px;box-shadow:0 22px 36px rgba(0,0,0,.16)}
.sticky::before{content:"";position:absolute;top:-24px;left:50%;width:190px;height:50px;margin-left:-95px;background:rgba(255,255,255,.6);box-shadow:0 1px 3px rgba(0,0,0,.12);transform:rotate(-3deg)}
.li{font-size:52px;line-height:1.5;font-weight:500;display:flex;gap:18px;margin-bottom:14px}
.li b{flex:none;color:#E2574C;font-weight:900}
.body{position:absolute;top:150px;right:200px;left:90px}
"""
def page(body, cls): return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='s {cls}'>{body}</div></body></html>"
HOLES = "".join(f"<div class='hole' style='top:{t}px'></div>" for t in (180, 650, 1120))
LOGO = f"<img src='data:image/png;base64,{b64('logo-white.png')}' style='position:absolute;top:70px;right:80px;height:70px'>"

def week(n, label, dates, title, items, note, color='#FFE98A', rot=-1.5):
    lis = "".join(f"<div class='li'><b>✓</b><span>{x}</span></div>" for x in items)
    return page(HOLES + f"<div class='body'><span class='wk'>{label}</span><span class='date'>{dates}</span><div class='title'>{title}</div></div>"
                + f"<div class='sticky' style='top:520px;background:{color};transform:rotate({rot}deg)'>{lis}</div>"
                + f"<div class='hand' style='position:absolute;bottom:120px;right:200px;left:90px;font-size:44px;color:#22524E;font-weight:700'>{note}</div>"
                + f"<div class='num'>{n}/7</div>", 'paper')

SLIDES = [
    page(LOGO + "<div style='position:absolute;top:96px;left:80px;font-family:L;font-weight:700;font-size:28px;letter-spacing:7px;color:#FFD84D;direction:ltr'>THE COUNTDOWN IS ON</div>"
         + "<div style='position:absolute;top:300px;left:0;right:0;text-align:center;font-size:62px;font-weight:800'>الامتحانات الفصلية بتبلّش 26/11</div>"
         + "<div style='position:absolute;top:400px;left:0;right:0;text-align:center;font-weight:900;font-size:230px;line-height:1;color:#FFD84D;white-space:nowrap'>3 أسابيع</div>"
         + "<div style='position:absolute;top:720px;left:0;right:0;text-align:center;font-size:66px;font-weight:900;line-height:1.3'>خطة الأهل،<br>أسبوع بأسبوع</div>"
         + "<div style='position:absolute;top:1050px;left:0;right:0;text-align:center'><span style='display:inline-block;background:#fff;color:#22524E;border-radius:999px;padding:18px 50px;font-size:46px;font-weight:800'>احفظوها واسحبوا 👈</span></div>", 'teal'),
    week(2, 'الأسبوع 1', '8/11 – 14/11', 'خريطة الطريق 🗺️',
         ['جدول الامتحانات على الحيط بغرفته', 'اسألوه: «شو أصعب 3 مواد عليك؟»', 'ساعة دراسة كل يوم، نفس الوقت'],
         'الهدف: ما في مفاجآت.'),
    week(3, 'الأسبوع 2', '15/11 – 21/11', 'تدريب مش قراءة ✍️',
         ['3 جلسات: 25 دقيقة دراسة + 5 راحة', 'التلفون برّا الغرفة وقت الدراسة', 'حلّ أسئلة… القراءة لحالها ما بتكفي'],
         'الفهم بيبان بالحلّ، مش بالقراءة.', '#CDEBD9', 1.2),
    week(4, 'الأسبوع 3', '22/11 – 28/11', 'امتحان تجريبي ⏱️',
         ['امتحان بالوقت لكل مادة كبيرة', 'نصحّحه سوا ونكتب الغلطات', 'الغلطة المكتوبة… ما بتنعاد'],
         'أول امتحانات الفترة: 26/11 و29/11.', '#FFE0C2', -1),
    week(5, 'أيام الامتحانات', '26/11 – 20/12', 'الليلة اللي قبل 🌙',
         ['مراجعة خفيفة للملخّص بس', 'نوم بكّير، والتلفون بالصالون', 'فطور… ولو إشي صغير'],
         'وبعد الامتحان: «كيف حسّيت؟» قبل «كم جبت؟»', '#E3E1FF', 1.5),
    page(HOLES + "<div class='body'><span class='wk'>وين رواد؟</span><div class='title'>إحنا معكم بكل أسبوع 💚</div></div>"
         + "<div class='sticky' style='top:520px;background:#FFE98A;transform:rotate(-1deg)'>"
         + "<div class='li'><b>📚</b><span>دروس تحضير فردي وجماعي لكل المواد</span></div>"
         + "<div class='li'><b>📝</b><span>امتحانات تجريبية على المنصة، بنمط المدرسة</span></div>"
         + "<div class='li'><b>🎯</b><span>تحدّي يومي من البيت على مادة الامتحان</span></div>"
         + "<div class='li'><b>📈</b><span>وإنتو بتشوفوا التقدّم من تلفونكم</span></div></div>"
         + "<div class='num'>6/7</div>", 'paper'),
    page(LOGO + "<div style='position:absolute;top:330px;left:0;right:0;text-align:center;font-size:110px;font-weight:900;line-height:1.2'>بلّش اليوم<br><span style='color:#FFD84D'>مش ليلة الامتحان</span></div>"
         + "<div style='position:absolute;top:690px;left:0;right:0;text-align:center;font-size:48px;font-weight:700;line-height:1.5;opacity:.92'>احفظوا الخطة 🔖 وابعتوها<br>لأهل عندهم ولد بامتحانات</div>"
         + "<div style='position:absolute;top:960px;left:150px;right:150px;background:#fff;color:#22524E;border-radius:999px;padding:24px 0;text-align:center'><div style='font-size:36px;color:#5E6E6B;font-weight:700'>احجزوا ساعاتكم قبل ما تمتلي</div><div style='font-family:L;font-size:80px;font-weight:900;direction:ltr'>054-6111668</div></div>", 'teal'),
]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for i, h in enumerate(SLIDES, 1):
        pg.set_content(h, wait_until='load'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        pg.screenshot(path=str(OUT / f'slide-{i}.png'))
    b.close()
print(len(SLIDES))
