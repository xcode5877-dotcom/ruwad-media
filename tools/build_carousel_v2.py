"""v2 of 'رسالة من ابنك': the kid's notebook — handwriting, crossed-out words, margin doodles, sticky notes."""
import base64, math, pathlib, random
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "2026-10-25-risala-min-ibnak-v2"
OUT.mkdir(parents=True, exist_ok=True)
NM = ROOT / "node_modules/@fontsource"

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

fonts = ""
for fam, pkg, weights in (("Rubik", "rubik", (400, 500, 700, 800)), ("Marhey", "marhey", (400, 600, 700)), ("Ruqaa", "aref-ruqaa", (400, 700))):
    for w in weights:
        for sub in ("arabic", "latin"):
            f = NM / pkg / "files" / f"{pkg}-{sub}-{w}-normal.woff2"
            if f.exists():
                fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"

LOGO_W = b64(ROOT / "logo-white.png")
LOGO_T = b64(ROOT / "logo-teal.png")

# ---------- hand-drawn SVG helpers ----------
rnd = random.Random(7)
def jit(a=3): return rnd.uniform(-a, a)

def smooth(pts, closed=False):
    """Catmull-Rom -> cubic bezier path through points."""
    if closed: pts = pts[-1:] + pts + pts[:2]
    else: pts = pts[:1] + pts + pts[-1:]
    d = f"M{pts[1][0]:.1f},{pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")

def hline(x1, y1, x2, y2, a=2.5, n=6):
    return smooth([(x1+(x2-x1)*i/n + (jit(a) if 0<i<n else 0), y1+(y2-y1)*i/n + (jit(a) if 0<i<n else 0)) for i in range(n+1)])

def hcircle(cx, cy, r, a=3, n=10, over=1.08):
    pts = [(cx + (r+jit(a))*math.cos(2*math.pi*i/n*over - 0.4), cy + (r+jit(a))*math.sin(2*math.pi*i/n*over - 0.4)) for i in range(n+1)]
    return smooth(pts)

def hrect(x, y, w, h, a=3):
    return hline(x, y, x+w, y, a) + " " + hline(x+w, y, x+w, y+h, a) + " " + hline(x+w, y+h, x, y+h, a) + " " + hline(x, y+h, x, y, a)

def path(d, color="#2B4C9B", w=5, fill="none", op=1):
    return f"<path d='{d}' stroke='{color}' stroke-width='{w}' fill='{fill}' stroke-linecap='round' stroke-linejoin='round' opacity='{op}'/>"

def svg(inner, w, h, style=""):
    return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' style='{style}' xmlns='http://www.w3.org/2000/svg'>{inner}</svg>"

# doodle icons (100x100 boxes)
def ic_phone_out(c):
    return path(hrect(28, 12, 44, 76, 2), c, 5) + path(hline(42, 76, 58, 76, 1), c, 5) + path(hline(10, 10, 90, 90, 2), "#E2574C", 7)
def ic_timer(c):
    return path(hcircle(50, 56, 36, 2), c, 5) + path(hline(50, 56, 50, 32, 1, 3), c, 5) + path(hline(50, 56, 66, 64, 1, 3), c, 5) + path(hline(40, 10, 60, 10, 1, 3), c, 6)
def ic_bubbles(c):
    return path(hrect(8, 14, 56, 38, 2), c, 5) + path(hline(20, 52, 14, 66, 1, 2), c, 5) + path(hrect(40, 48, 52, 34, 2), c, 5) + path(hline(80, 82, 88, 94, 1, 2), c, 5)
def ic_moon(c):
    return path("M62,14 C30,18 18,52 34,74 C48,92 78,90 90,70 C66,76 46,58 50,36 C52,26 56,18 62,14 Z", c, 5) + \
           f"<text x='8' y='34' font-family='Marhey' font-size='26' fill='{c}'>z</text><text x='18' y='16' font-family='Marhey' font-size='20' fill='{c}'>z</text>"
def ic_hands(c):
    return path("M50,86 C20,64 8,46 18,30 C26,18 42,20 50,34 C58,20 74,18 82,30 C92,46 80,64 50,86 Z", "#E2574C", 6)

CSS = fonts + """
:root{--teal:#22524E;--teal-d:#14332F;--paper:#FFFDF6;--line:#CFE0EE;--margin:#F2A7A7;--ink:#24345E;--pen:#2B4C9B;--hl:#FFE36E;--accent:#F0A04B;--red:#E2574C}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Rubik,sans-serif;direction:rtl;color:#1A2B29}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden}
.paper{background-color:var(--paper);
  background-image:linear-gradient(transparent 0 calc(100% - 3px), var(--line) calc(100% - 3px));
  background-size:100% 72px;background-position:0 38px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:150px;width:4px;background:var(--margin);opacity:.8}
.holes span{position:absolute;right:52px;width:44px;height:44px;border-radius:50%;background:#E9E3D6;box-shadow:inset 0 3px 6px rgba(0,0,0,.18)}
.hand{font-family:Marhey;color:var(--pen)}
.pg{position:absolute;bottom:52px;left:70px;font-family:Marhey;font-size:34px;color:var(--pen);opacity:.7;direction:ltr}
.logo{position:absolute;height:54px}
.hl{background:linear-gradient(transparent 52%, rgba(255,227,110,.9) 52%, rgba(255,227,110,.9) 92%, transparent 92%);padding:0 10px}
/* cover */
.night{background:radial-gradient(circle at 26% 74%, rgba(255,205,120,.55) 0, rgba(255,205,120,.12) 32%, transparent 55%), linear-gradient(180deg,#0F2826 0%,#1B4642 100%);color:#fff}
.cover-h{position:absolute;top:150px;right:90px;left:90px}
.cover-h .a{font-size:96px;font-weight:800;line-height:1.15}
.cover-h .b{font-family:Marhey;font-weight:700;font-size:88px;color:var(--hl);margin-top:14px;display:inline-block;transform:rotate(-3deg)}
.notif{position:absolute;top:620px;right:110px;width:820px;background:rgba(255,255,255,.97);color:#1A2B29;border-radius:40px;padding:30px 36px;display:flex;gap:26px;align-items:center;box-shadow:0 0 0 10px rgba(255,255,255,.08),0 30px 80px rgba(0,0,0,.45);transform:rotate(2deg)}
.notif .app{width:88px;height:88px;border-radius:24px;background:var(--accent);flex:none;display:flex;align-items:center;justify-content:center;font-family:Marhey;font-size:46px;font-weight:700;color:#fff}
.notif .t{display:flex;justify-content:space-between;font-size:30px;color:#6B7775}
.notif .t b{color:#1A2B29;font-size:34px}
.notif .m{font-size:38px;font-weight:500;line-height:1.4;margin-top:4px}
/* letter */
.letter{position:absolute;top:110px;right:200px;left:80px}
.letter p{font-family:Marhey;color:var(--pen);font-size:54px;line-height:72px;font-weight:500}
.strike{position:relative;display:inline-block;color:#7E8FB8}.strike svg{position:absolute;inset:6px -8px 0 -8px;width:calc(100% + 16px);height:80%}
.sticky{position:absolute;padding:44px 48px 40px;box-shadow:0 18px 30px rgba(0,0,0,.16), 0 2px 0 rgba(0,0,0,.05)}
.sticky::before{content:"";position:absolute;top:-22px;left:50%;width:170px;height:46px;margin-left:-85px;background:rgba(255,255,255,.55);box-shadow:0 1px 3px rgba(0,0,0,.12);transform:rotate(-3deg)}
.y{background:#FFE98A}.m2{background:#CDEBD9}.p{background:#FFD6BA}.bl{background:#D6E6FB}
.sticky h3{font-family:Marhey;font-weight:700;font-size:58px;line-height:1.2;color:#1D2B3A}
.sticky p{font-size:40px;line-height:1.5;margin-top:16px;color:#26323A}
.sticky .n{position:absolute;top:26px;left:34px;font-family:Marhey;font-weight:700;font-size:64px;color:rgba(0,0,0,.18)}
.sticky .ic{position:absolute;bottom:26px;left:30px}
.title{position:absolute;top:96px;right:200px;font-family:Marhey;font-weight:700;font-size:66px;color:var(--ink)}
/* cta */
.cta{background:var(--teal);color:#fff}
.chalk{position:absolute;inset:0}
.cta .q{position:absolute;top:330px;right:90px;left:90px;text-align:center;font-family:Marhey;font-weight:700;font-size:96px;line-height:1.2}
.cta .s{position:absolute;top:620px;right:90px;left:90px;text-align:center;font-size:44px;line-height:1.55}
.wa{position:absolute;top:820px;left:130px;right:130px;background:#fff;color:var(--teal);border-radius:999px;padding:30px 0;text-align:center;transform:rotate(-1.5deg);box-shadow:0 20px 40px rgba(0,0,0,.25)}
.wa small{display:block;font-size:32px;font-weight:500;color:#5E6E6B}
.wa b{display:block;font-size:80px;font-weight:800;direction:ltr;letter-spacing:2px}
.place{position:absolute;top:1080px;left:0;right:0;text-align:center;font-size:36px;opacity:.85}
"""

def page(body, cls):
    return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='slide {cls}'>{body}</div></body></html>"

def holes(): return "<div class='holes'>" + "".join(f"<span style='top:{y}px'></span>" for y in (180, 640, 1100)) + "</div>"
def pg(n): return f"<div class='pg'>{n}/6</div>"

slides = []

# ---- 1. cover: night, desk lamp, phone lights up ----
scene = ""
# desk
scene += "<rect x='0' y='560' width='1080' height='240' fill='#0B1F1D'/><rect x='0' y='556' width='1080' height='8' fill='#2E5A55'/>"
# lamp
scene += path("M150,556 L150,540 C150,530 250,530 250,540 L250,556 Z", "#0B1F1D", 0, fill="#2A4F4B")
scene += path(hline(200, 536, 250, 330, 1, 3), "#2A4F4B", 14) + path(hline(250, 330, 360, 250, 1, 3), "#2A4F4B", 14)
scene += "<path d='M330,200 L460,250 L400,340 L290,290 Z' fill='#E9A84E'/><ellipse cx='370' cy='318' rx='42' ry='18' fill='#FFF3C4'/>"
# open notebook
scene += "<path d='M420,520 L650,500 L650,640 L395,660 Z' fill='#FFFDF6'/><path d='M650,500 L890,520 L915,660 L650,640 Z' fill='#F4F0E6'/>"
for i in range(6):
    y1 = 528 + i*20
    scene += f"<line x1='{424-i*4}' y1='{y1+4}' x2='640' y2='{y1-12}' stroke='#CFE0EE' stroke-width='3'/>"
    scene += f"<line x1='660' y1='{y1-12}' x2='{892+i*4}' y2='{y1+4}' stroke='#CFE0EE' stroke-width='3'/>"
scene += "<path d='M650,500 L650,640' stroke='#D9D2C2' stroke-width='4'/>"
scene += path("M470,560 C500,550 540,575 580,556", "#2B4C9B", 4) + path("M470,590 C510,580 530,598 560,588", "#2B4C9B", 4, op=.7)
# pencil
scene += "<g transform='rotate(-18 560 680)'><rect x='440' y='668' width='230' height='22' rx='4' fill='#F0A04B'/><path d='M670,668 L708,679 L670,690 Z' fill='#F5D7B0'/><path d='M697,676 L708,679 L697,682 Z' fill='#333'/><rect x='420' y='668' width='24' height='22' rx='3' fill='#E2574C'/></g>"
# phone on the right page, glowing
scene += "<g transform='rotate(-14 800 590)'><ellipse cx='800' cy='590' rx='170' ry='120' fill='rgba(190,230,255,.25)'/><rect x='735' y='480' width='130' height='230' rx='22' fill='#0A0F14'/><rect x='745' y='494' width='110' height='202' rx='14' fill='#DCEFFF'/><rect x='755' y='520' width='90' height='26' rx='8' fill='#F0A04B'/></g>"
slides.append(page(
    f"<img class='logo' style='top:64px;right:90px' src='data:image/png;base64,{LOGO_W}'>"
    "<div class='cover-h'><div class='a'>الرسالة اللي ابنك<br>ما رح يبعتها</div><div class='b'>بفترة الامتحانات</div></div>"
    + svg(scene, 1080, 800, "position:absolute;bottom:0;left:0")
    + "<div class='notif'><div class='app'>ا</div><div style='flex:1'><div class='t'><b>ابني</b><span>الآن</span></div><div class='m'>يمّا… بدي أحكيلك إشي، بس لا تعصّبي</div></div></div>"
    + "<div class='pg' style='color:#fff'>1/6</div>"
    + "<div class='hand' style='position:absolute;bottom:50px;right:90px;font-size:40px;color:#FFE36E'>اقرأوها للآخر ←</div>",
    "night"))

# ---- 2. the letter in his notebook ----
strike1 = "<svg viewBox='0 0 340 70' preserveAspectRatio='none'>" + path(hline(4, 40, 336, 30, 3, 8), "#2B4C9B", 6) + path(hline(6, 22, 334, 48, 3, 8), "#2B4C9B", 5) + "</svg>"
margin_doodles = svg(
    path(hcircle(60, 60, 34, 3), "#2B4C9B", 4) + path(hline(46, 54, 47, 55, 0.5, 1), "#2B4C9B", 7) + path(hline(72, 54, 73, 55, 0.5, 1), "#2B4C9B", 7) + path("M46,78 C54,70 66,70 74,78", "#2B4C9B", 4)
    + f"<text x='14' y='190' font-family='Marhey' font-size='34' fill='#2B4C9B' opacity='.75'>x²+3x</text>" + path(hline(8, 176, 120, 168, 2, 4), "#2B4C9B", 4, op=.75)
    + path("M30,300 L48,262 L66,300 L24,276 L72,276 Z", "#F0A04B", 4)
    + path(hrect(22, 380, 60, 100, 3), "#2B4C9B", 4) + path(hline(42, 464, 62, 464, 1, 2), "#2B4C9B", 4) + f"<text x='36' y='420' font-family='Marhey' font-size='30' fill='#E2574C'>!</text>",
    120, 520, "position:absolute;top:150px;right:18px")
slides.append(page(
    holes()
    + "<div class='letter'><p>"
      "يمّا،<br>"
      "عندي امتحان بكرا.<br>"
      "بقعد أدرس… وبعد 5 دقايق<br>بلاقي حالي عالتلفون.<br>"
      f"<span class='strike'>أنا ولد كسلان{strike1}</span><br>"
      "مش قصدي، والله بدي أنجح.<br>"
      "بس راسي مليان ضجة.<br>"
      "ساعدوني… بس بدون صريخ."
      "</p>"
      f"<div class='hand' style='font-size:50px;margin-top:20px;display:flex;gap:16px;align-items:center'>ابنك {svg(ic_hands('#E2574C'),70,70)}</div></div>"
    + margin_doodles
    + "<div class='sticky y' style='bottom:120px;left:80px;width:640px;transform:rotate(-2.5deg)'><p style='margin:0;font-size:38px'>كثير ولاد بحسّوا هيك بعد سنين الكورونا والحرب.<br><b>المشكلة مش إنهم ما بدهم يدرسوا.</b></p></div>"
    + pg(2), "paper"))

# ---- 3-5. sticky-note tips ----
def tip(n, cls, h, p, ic, style):
    return (f"<div class='sticky {cls}' style='{style}'><div class='n'>{n}</div><h3>{h}</h3><p>{p}</p>"
            f"<div class='ic'>{svg(ic, 100, 100)}</div></div>")

title_hl = svg(path(hline(0, 30, 560, 22, 4, 8), "#FFE36E", 40, op=.85), 580, 60, "position:absolute;top:150px;right:190px")
def tips_page(n, body):
    return page(holes() + title_hl + "<div class='title'>5 أشياء بتفرق الليلة</div>" + body + pg(n), "paper")

slides.append(tips_page(3,
    tip(1, "y", "التلفون برّا الغرفة", "مش مقلوب على الطاولة. حتى وهو ساكت، بيضل يشدّ انتباهه.", ic_phone_out("#1D2B3A"),
        "top:300px;right:200px;width:760px;min-height:400px;padding-left:170px;transform:rotate(1.8deg)")
    + tip(2, "m2", "25 دقيقة دراسة،<br>5 دقايق راحة", "والراحة بعيد عن الشاشة: كاسة مَي، مشوار بالبيت، إشي ياكله.", ic_timer("#1D2B3A"),
        "top:780px;right:240px;width:760px;min-height:420px;padding-left:170px;transform:rotate(-2deg)")))

slides.append(tips_page(4,
    tip(3, "p", "غيّروا السؤال", "بدل «درست؟» اسألوه «شو أصعب سؤال لهلأ؟». الأول بيسكّر الحديث، والثاني بيفتحه.", ic_bubbles("#1D2B3A"),
        "top:300px;right:220px;width:760px;min-height:420px;padding-left:170px;transform:rotate(-1.6deg)")
    + tip(4, "bl", "النوم جزء من الدراسة", "نوم بكّير قبل الامتحان بيفيده أكثر من ساعة حفظ زيادة بآخر الليل.", ic_moon("#1D2B3A"),
        "top:800px;right:190px;width:760px;min-height:380px;padding-left:170px;transform:rotate(2.2deg)")))

closing_underline = svg(path(hline(0, 20, 640, 10, 5, 10), "#E2574C", 9), 660, 40, "position:absolute;top:1090px;right:220px")
slides.append(tips_page(5,
    tip(5, "y", "إذا علق،<br>مش وقت عصبية", "اقعدوا جنبه عشر دقايق. وإذا المادة صعبة عليكم كمان، دوّروا مع بعض على مين يشرحله.", ic_hands("#1D2B3A"),
        "top:300px;right:220px;width:760px;min-height:460px;padding-left:170px;transform:rotate(-1.8deg)")
    + "<div class='hand' style='position:absolute;top:880px;right:220px;font-size:76px;font-weight:700;line-height:1.25;color:#22524E'>التلفون مش العدو.<br>بس الليلة مش وقته.</div>"
    + closing_underline))

# ---- 6. CTA: chalk doodles on teal ----
chalk = ""
chalk += path(hcircle(150, 230, 50, 4), "rgba(255,255,255,.35)", 5) + path(hline(130, 230, 170, 230, 2, 3), "rgba(255,255,255,.35)", 5)
chalk += path("M920,200 L940,160 L960,200 L912,176 L968,176 Z", "#FFE36E", 5, op=.8)
chalk += path("M880,1180 L900,1140 L920,1180 L872,1156 L928,1156 Z", "rgba(255,255,255,.35)", 5)
chalk += path(hrect(120, 1110, 70, 120, 4), "rgba(255,255,255,.35)", 5)
chalk += path("M820,930 C900,900 960,860 970,780", "#FFE36E", 6) + path("M948,800 L970,776 L986,806", "#FFE36E", 6)
chalk += f"<text x='90' y='760' font-family='Marhey' font-size='60' fill='rgba(255,255,255,.18)' direction='ltr'>A+</text>"
chalk += f"<text x='900' y='300' font-family='Marhey' font-size='54' fill='rgba(255,255,255,.18)' direction='ltr'>√x</text>"
slides.append(page(
    svg(chalk, 1080, 1350, "position:absolute;inset:0")
    + f"<img class='logo' style='top:110px;right:50%;margin-right:-110px;height:120px' src='data:image/png;base64,{LOGO_W}'>"
    + "<div class='q'>علق بمادة<br>قبل الامتحان؟</div>"
    + "<div class='s'>دروس قبل الامتحان بحجز مسبق<br>فردي وجماعي، لكل الصفوف</div>"
    + "<div class='wa'><small>احجزوا على واتساب</small><b>054-6111668</b></div>"
    + "<div class='place'>معهد رُوّاد · دبورية</div>"
    + "<div class='pg' style='color:#fff'>6/6</div>", "cta"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pgx = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(slides, 1):
        pgx.set_content(html, wait_until="load")
        pgx.evaluate("document.fonts.ready")
        pgx.wait_for_timeout(150)
        pgx.screenshot(path=str(OUT / f"slide-{i}.png"))
    b.close()
print(OUT)
