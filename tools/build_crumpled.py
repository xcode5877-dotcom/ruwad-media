"""Carousel 2026-11-01: الورقة المكرمشة — what to say when your kid brings home a low grade. 1080x1350, notebook style."""
import base64, math, pathlib, random
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "2026-11-01-crumpled-paper"
OUT.mkdir(parents=True, exist_ok=True)
NM = ROOT / "node_modules/@fontsource"
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
fonts = ""
for fam, pkg, ws in (("Rubik", "rubik", (400, 500, 700, 800)), ("Marhey", "marhey", (400, 500, 700))):
    for w in ws:
        for sub in ("arabic", "latin"):
            f = NM / pkg / "files" / f"{pkg}-{sub}-{w}-normal.woff2"
            if f.exists():
                fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"
LOGO_W = b64(ROOT / "logo-white.png"); LOGO_T = b64(ROOT / "logo-teal.png")

rnd = random.Random(11)
def jit(a=3): return rnd.uniform(-a, a)
def smooth(pts):
    pts = pts[:1] + pts + pts[-1:]
    d = f"M{pts[1][0]:.1f},{pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d
def hline(x1, y1, x2, y2, a=2.5, n=6):
    return smooth([(x1+(x2-x1)*i/n + (jit(a) if 0<i<n else 0), y1+(y2-y1)*i/n + (jit(a) if 0<i<n else 0)) for i in range(n+1)])
def path(d, c="#2B4C9B", w=5, fill="none", op=1):
    return f"<path d='{d}' stroke='{c}' stroke-width='{w}' fill='{fill}' stroke-linecap='round' stroke-linejoin='round' opacity='{op}'/>"

def crumpled(W, H, cols=7, rows=9, amp=26, seed=3, lo=0.86):
    """Low-poly crumpled sheet: jittered grid, triangles shaded by random light."""
    r = random.Random(seed)
    pts = [[(W*i/cols + (r.uniform(-amp, amp) if 0<i<cols else 0) + (r.uniform(-10,10) if i in (0,cols) else 0),
             H*j/rows + (r.uniform(-amp, amp) if 0<j<rows else 0) + (r.uniform(-10,10) if j in (0,rows) else 0))
            for i in range(cols+1)] for j in range(rows+1)]
    out = ""
    for j in range(rows):
        for i in range(cols):
            a, b, c, d = pts[j][i], pts[j][i+1], pts[j+1][i+1], pts[j+1][i]
            for tri in ((a, b, c), (a, c, d)) if (i+j) % 2 else ((a, b, d), (b, c, d)):
                L = r.uniform(lo, 1.0)
                col = f"rgb({int(255*L)},{int(253*L)},{int(246*L)})"
                out += f"<polygon points='{' '.join(f'{x:.1f},{y:.1f}' for x,y in tri)}' fill='{col}' stroke='{col}' stroke-width='1'/>"
    # faint ruled lines following the sheet
    for k in range(1, 12):
        y = H*k/12
        out += f"<path d='{hline(10, y, W-10, y+r.uniform(-8,8), 9, 7)}' stroke='#CFE0EE' stroke-width='3' fill='none' opacity='.8'/>"
    out += f"<path d='{hline(W-80, 6, W-86, H-6, 8, 8)}' stroke='#F2A7A7' stroke-width='4' fill='none'/>"
    return out

CSS = fonts + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Rubik;direction:rtl;color:#1A2B29}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden}
.desk{background:radial-gradient(circle at 60% 45%,#2B5E59 0,#163A37 70%)}
.paper{background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px),#CFE0EE calc(100% - 3px));background-size:100% 72px;background-position:0 38px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:150px;width:4px;background:#F2A7A7;opacity:.8}
.holes span{position:absolute;right:52px;width:44px;height:44px;border-radius:50%;background:#E9E3D6;box-shadow:inset 0 3px 6px rgba(0,0,0,.18)}
.hand{font-family:Marhey;color:#2B4C9B}
.pg{position:absolute;bottom:52px;left:70px;font-family:Marhey;font-size:34px;color:#2B4C9B;opacity:.7;direction:ltr}
.logo{position:absolute;height:54px}
.kicker{position:absolute;top:100px;right:200px;font-family:Marhey;font-weight:700;font-size:56px;color:#24345E}
.said{position:absolute;top:290px;right:200px;left:90px}
.said .q{font-family:Marhey;font-size:76px;line-height:1.4;color:#7E8FB8;text-decoration:line-through;text-decoration-color:#E2574C;text-decoration-thickness:6px}
.said .lbl{font-size:36px;font-weight:700;color:#E2574C;margin-bottom:18px;display:block}
.arrow{position:absolute;right:420px}
.sticky{position:absolute;right:200px;left:110px;padding:46px 52px 50px;box-shadow:0 18px 30px rgba(0,0,0,.16)}
.sticky::before{content:"";position:absolute;top:-22px;left:50%;width:170px;height:46px;margin-left:-85px;background:rgba(255,255,255,.6);box-shadow:0 1px 3px rgba(0,0,0,.12);transform:rotate(-3deg)}
.sticky .lbl{font-size:36px;font-weight:700;color:#22524E;display:block;margin-bottom:14px}
.sticky h3{font-family:Marhey;font-weight:700;font-size:70px;line-height:1.3;color:#1D2B3A}
.sticky p{font-size:44px;line-height:1.5;margin-top:24px;color:#33414A}
.y{background:#FFE98A}.m{background:#CDEBD9}.o{background:#FFD6BA}.b{background:#D6E6FB}
.cta{background:#22524E;color:#fff}
"""
def page(body, cls): return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='slide {cls}'>{body}</div></body></html>"
def holes(): return "<div class='holes'>" + "".join(f"<span style='top:{y}px'></span>" for y in (180, 640, 1100)) + "</div>"
def pg(n, c="#2B4C9B"): return f"<div class='pg' style='color:{c}'>{n}/7</div>"

slides = []

# 1 cover: crumpled exam on the desk
sheet = crumpled(700, 900)
for k, y in enumerate((230, 330, 430, 530)):
    sheet += path(hline(120, y, 560 - k*40, y + jit(6), 4, 6), "#2B4C9B", 5, op=.55)
    sheet += path(hline(80, y-28, 110, y-2, 1, 2) + " " + hline(80, y-2, 110, y-28, 1, 2), "#E2574C", 7)
sheet += "<text x='175' y='800' font-family='Marhey' font-weight='700' font-size='190' fill='#E2574C' text-anchor='middle'>54</text>"
sheet += path(smooth([(175+170*math.cos(a)+jit(5), 735+105*math.sin(a)+jit(5)) for a in [i*2*math.pi/12 - 0.3 for i in range(14)]]), "#E2574C", 9)
cover_svg = f"<svg width='700' height='900' viewBox='0 0 700 900' style='position:absolute;top:330px;left:110px;transform:rotate(-7deg);filter:drop-shadow(0 30px 40px rgba(0,0,0,.45))'>{sheet}</svg>"
slides.append(page(
    f"<img class='logo' style='top:64px;right:90px' src='data:image/png;base64,{LOGO_W}'>"
    + cover_svg
    + "<div style='position:absolute;top:400px;left:190px;width:520px;transform:rotate(-7deg);font-family:Marhey;font-size:40px;color:#2B4C9B;text-align:right'>امتحان رياضيات · الصف السابع</div>"
    + "<div style='position:absolute;top:160px;right:90px;left:90px;color:#fff;font-weight:800;font-size:90px;line-height:1.2'>ابنك جاب علامة واطية؟</div>"
    + "<div style='position:absolute;top:1080px;right:70px;width:520px;background:#FFD84D;color:#14332F;font-family:Marhey;font-weight:700;font-size:58px;line-height:1.3;padding:26px 36px 34px;border-radius:16px 28px 18px 30px;transform:rotate(3deg);box-shadow:0 16px 36px rgba(0,0,0,.4)'>أول جملة بتحكوها…<br>بتفرق كثير.</div>"
    + pg(1, "#fff"), "desk"))

pairs = [
    ("ليش هيك؟! شو كنت عامل كل هالوقت؟", "شكلك زعلان. بدك نحكي؟", "قبل أي سؤال عن الدراسة، خلّوه يحس إنكم معه مش ضده.", "y"),
    ("شوف ابن عمك جاب 90!", "خلّينا نشوف سوا وين علقت.", "المقارنة بتعلّمه يخبّي علاماته. السؤال بيعلّمه يدوّر على الغلط.", "m"),
    ("خلص! ما في تلفون شهر.", "شو بدك يتغيّر للامتحان الجاي؟", "العقوبة بتسكّر الموضوع. الخطة بتفتحه، وهو بيشارك فيها.", "o"),
    ("إنت أصلًا مش شاطر بالرياضيات.", "هاي المادة بدها شغل أكثر، ومنقدر عليها.", "الجملة اللي بيسمعها كثير، بيصدّقها عن حاله.", "b"),
]
for n, (bad, good, why, col) in enumerate(pairs, 2):
    strike = f"<svg viewBox='0 0 600 100' preserveAspectRatio='none' style='position:absolute;inset:10px -10px 0 -10px;width:calc(100% + 20px);height:85%'>{path(hline(4, 55, 596, 45, 4, 10), '#E2574C', 9)}</svg>"
    arrow = f"<svg class='arrow' width='160' height='170' style='top:{575}px'>{path('M80,10 C60,60 100,100 80,140', '#E2574C', 8)}{path('M52,112 L80,150 L108,110', '#E2574C', 8)}</svg>"
    slides.append(page(
        holes()
        + "<div class='kicker'>بدل ما تقولوا…</div>"
        + f"<div class='said'><span class='lbl'>✗ الجملة اللي بتطلع لحالها</span><span class='q'>«{bad}»</span></div>"
        + arrow
        + f"<div class='sticky {col}' style='top:770px;transform:rotate({[-1.8,1.6,-1.4,1.9][n-2]}deg)'><span class='lbl'>✓ جرّبوا:</span><h3>«{good}»</h3><p>{why}</p></div>"
        + pg(n), "paper"))

# 6 the paper smooths out
flat = crumpled(700, 520, cols=7, rows=5, amp=5, seed=9, lo=0.95)
slides.append(page(
    holes()
    + f"<svg width='700' height='520' style='position:absolute;top:150px;left:150px;transform:rotate(-2deg);filter:drop-shadow(0 18px 24px rgba(0,0,0,.18))'>{flat}"
      "</svg><div style='position:absolute;top:150px;left:150px;width:700px;height:520px;transform:rotate(-2deg);display:flex;align-items:center;justify-content:center;gap:34px;direction:rtl'><span style='font-family:Marhey;font-weight:700;font-size:170px;color:#E2574C'>54</span><span style='font-family:Marhey;font-size:76px;color:#2B4C9B'>= امتحان واحد</span></div>"
    + "<div class='hand' style='position:absolute;top:780px;right:200px;left:90px;font-size:80px;font-weight:700;line-height:1.3;color:#22524E'>العلامة رقم عن امتحان.<br>مش رقم عن ابنك.</div>"
    + f"<svg width='640' height='40' style='position:absolute;top:1010px;right:200px'>{path(hline(0, 20, 620, 12, 5, 10), '#E2574C', 9)}</svg>"
    + "<div style='position:absolute;top:1090px;right:200px;left:90px;font-size:42px;line-height:1.5'>احفظوا البوست للمرة الجاية،<br>وابعتوه لحدا ابنه بامتحانات هالفترة.</div>"
    + pg(6), "paper"))

# 7 CTA
slides.append(page(
    f"<img style='display:block;height:130px;margin:170px auto 0' src='data:image/png;base64,{LOGO_W}'>"
    + "<div style='text-align:center;font-family:Marhey;font-weight:700;font-size:92px;line-height:1.2;margin-top:110px'>بدكم تعرفوا<br>وين علق بالزبط؟</div>"
    + "<div style='text-align:center;font-size:44px;line-height:1.55;margin-top:40px'>ابعتولنا المادة والصف،<br>ومنحكيلكم من وين منبلّش.</div>"
    + "<div style='margin:70px auto 0;background:#fff;color:#22524E;border-radius:999px;width:820px;padding:30px 0;text-align:center;transform:rotate(-1.5deg)'><div style='font-size:32px;color:#5E6E6B'>واتساب</div><div style='font-size:78px;font-weight:800;direction:ltr'>054-6111668</div></div>"
    + "<div style='text-align:center;font-size:36px;margin-top:50px;opacity:.85'>دروس تقوية فردي وجماعي · معهد رُوّاد · دبورية</div>"
    + pg(7, "#fff"), "cta"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pgx = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(slides, 1):
        pgx.set_content(html, wait_until="load"); pgx.evaluate("document.fonts.ready"); pgx.wait_for_timeout(120)
        pgx.screenshot(path=str(OUT / f"slide-{i}.png"))
    b.close()
print(OUT)
