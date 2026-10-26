"""Daily Instagram/Facebook stories for RUWAD, 1080x1920 PNG. Safe zones: top 250px, bottom 330px kept clear of key content.
Interactivity without stickers: every interactive story asks for a reply (DM), which Instagram counts as a strong signal."""
import base64, json, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "stories"; OUT.mkdir(parents=True, exist_ok=True)
NM = ROOT / "node_modules/@fontsource"
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
fonts = ""
for fam, pkg, ws in (("Rubik", "rubik", (400, 500, 700, 800)), ("Marhey", "marhey", (500, 700))):
    for w in ws:
        for sub in ("arabic", "latin"):
            f = NM / pkg / "files" / f"{pkg}-{sub}-{w}-normal.woff2"
            if f.exists():
                fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"
LOGO_W = b64(ROOT / "logo-white.png"); LOGO_T = b64(ROOT / "logo-teal.png")

CSS = fonts + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:Rubik;direction:rtl;color:#1A2B29}
.s{width:1080px;height:1920px;position:relative;overflow:hidden}
.paper{background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px),#CFE0EE calc(100% - 3px));background-size:100% 90px;background-position:0 40px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:130px;width:4px;background:#F2A7A7;opacity:.8}
.teal{background:radial-gradient(circle at 50% 35%,#2B5E59 0,#163A37 75%);color:#fff}
.logo{position:absolute;top:270px;right:90px;height:62px}
.chip{display:inline-block;font-weight:800;font-size:44px;padding:14px 34px;border-radius:999px}
.hand{font-family:Marhey}
.q{position:absolute;top:420px;right:180px;left:80px}
.opts{position:absolute;top:760px;right:180px;left:80px;display:flex;flex-direction:column;gap:24px}
.opt{background:#fff;border:5px solid #22524E;border-radius:30px;padding:16px 36px;font-size:58px;font-weight:700;display:flex;gap:30px;align-items:center;box-shadow:0 8px 0 #22524E}
.opt b{width:90px;height:90px;border-radius:50%;background:#22524E;color:#fff;display:flex;align-items:center;justify-content:center;font-family:Rubik;font-weight:800;font-size:50px;flex:none}
.reply{position:absolute;bottom:330px;left:80px;right:80px;text-align:center;background:#FFD84D;color:#14332F;font-weight:800;font-size:54px;padding:30px 20px;border-radius:24px;transform:rotate(-1.5deg);box-shadow:0 14px 30px rgba(0,0,0,.18)}
.sticky{position:absolute;padding:60px 64px;box-shadow:0 22px 36px rgba(0,0,0,.18)}
.sticky::before{content:"";position:absolute;top:-26px;left:50%;width:200px;height:54px;margin-left:-100px;background:rgba(255,255,255,.6);box-shadow:0 1px 3px rgba(0,0,0,.12);transform:rotate(-3deg)}
.wa{position:absolute;bottom:360px;left:120px;right:120px;background:#fff;color:#22524E;border-radius:999px;padding:24px 0;text-align:center}
.wa small{display:block;font-size:34px;color:#5E6E6B}.wa b{font-size:76px;font-weight:800;direction:ltr;display:block}
"""
def page(body, cls): return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='s {cls}'>{body}</div></body></html>"
LT = f"<img class='logo' src='data:image/png;base64,{LOGO_T}'>"
LW = f"<img class='logo' src='data:image/png;base64,{LOGO_W}'>"

def quiz(tag, q, opts, ltr=False):
    d = "direction:ltr;text-align:left;" if ltr else ""
    o = "".join(f"<div class='opt' style='{d}'><b>{l}</b><span style='{d}'>{t}</span></div>" for l, t in zip("أبجد", opts))
    return page(LT + f"<div style='position:absolute;top:290px;left:80px'><span class='chip' style='background:#E2574C;color:#fff'>{tag}</span></div>"
                + f"<div class='q hand' style='font-size:84px;font-weight:700;line-height:1.3;color:#24345E;{d}'>{q}</div>"
                + f"<div class='opts'>{o}</div>"
                + "<div class='reply'>ردّوا على الستوري بالحرف 👇<br><span style='font-size:40px;font-weight:500'>الجواب بكرا</span></div>", "paper")

def answer(tag, q, ans, why, ltr=False):
    d = "direction:ltr;" if ltr else ""
    return page(LT + f"<div style='position:absolute;top:290px;left:80px'><span class='chip' style='background:#22524E;color:#fff'>{tag}</span></div>"
                + f"<div class='q hand' style='font-size:66px;line-height:1.3;color:#7E8FB8;{d}'>{q}</div>"
                + f"<div class='hand' style='position:absolute;top:760px;right:180px;left:80px;text-align:center;font-size:190px;font-weight:700;color:#E2574C;{d}'>{ans}</div>"
                + f"<div class='sticky' style='top:1100px;right:170px;left:90px;background:#CDEBD9;transform:rotate(-1.5deg)'><div style='font-size:50px;line-height:1.5;font-weight:500'>{why}</div></div>", "paper")

def countdown(n):
    return page(LW + "<div style='position:absolute;top:560px;left:0;right:0;text-align:center'>"
                + f"<div style='font-weight:800;font-size:360px;line-height:1;direction:ltr'>{n}</div>"
                + "<div class='hand' style='font-size:96px;font-weight:700;margin-top:10px'>يوم</div>"
                + "<div style='margin-top:40px'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:60px'>للبجروت الشتوي</span></div>"
                + "<div style='font-size:46px;margin-top:70px;line-height:1.55;opacity:.95'>الصف الحادي عشر والثاني عشر<br>التحضير برواد فردي وجماعي</div></div>"
                + "<div class='wa'><small>احجزوا مكانكم على واتساب</small><b>054-6111668</b></div>", "teal")

def tip(title, body, color="#FFE98A"):
    return page(LT + "<div style='position:absolute;top:300px;left:80px'><span class='chip' style='background:#22524E;color:#fff'>نصيحة الليلة للأهل</span></div>"
                + f"<div class='sticky' style='top:560px;right:170px;left:90px;background:{color};transform:rotate(1.8deg)'>"
                + f"<div class='hand' style='font-size:92px;font-weight:700;line-height:1.25;color:#1D2B3A'>{title}</div>"
                + f"<div style='font-size:52px;line-height:1.55;margin-top:34px;color:#33414A'>{body}</div></div>"
                + "<div class='reply' style='background:#fff;border:5px solid #22524E'>بتجرّبوها الليلة؟ ردّوا بـ 💚</div>", "paper")

def poll(q, opts):
    o = "".join(f"<div class='opt'><b>{i}</b><span>{t}</span></div>" for i, t in enumerate(opts, 1))
    return page(LT + "<div style='position:absolute;top:290px;left:80px'><span class='chip' style='background:#F0A04B;color:#fff'>سؤال للأهل</span></div>"
                + f"<div class='q hand' style='font-size:80px;font-weight:700;line-height:1.3;color:#24345E'>{q}</div>"
                + f"<div class='opts' style='top:760px'>{o}</div>"
                + "<div class='reply'>ردّوا بالرقم 👇<br><span style='font-size:40px;font-weight:500'>منشارككم النتيجة بمنشور</span></div>", "paper")

def newpost(cover, label):
    return page(LW + "<div style='position:absolute;top:420px;left:0;right:0;text-align:center'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:56px'>" + label + "</span></div>"
                + f"<img src='data:image/jpeg;base64,{b64(ROOT / cover)}' style='position:absolute;top:560px;left:50%;width:480px;margin-left:-240px;border-radius:34px;border:10px solid #fff;transform:rotate(-3deg);box-shadow:0 30px 60px rgba(0,0,0,.45)'>"
                + "<div class='hand' style='position:absolute;bottom:380px;left:0;right:0;text-align:center;font-size:64px;font-weight:700'>هسا على الصفحة ↑</div>", "teal")

def weekend(title, body):
    return page(LW + f"<div class='hand' style='position:absolute;top:520px;right:90px;left:90px;font-size:110px;font-weight:700;line-height:1.2'>{title}</div>"
                + f"<div style='position:absolute;top:860px;right:90px;left:90px;font-size:54px;line-height:1.6'>{body}</div>"
                + "<div class='wa'><small>دروس تقوية لكل الصفوف · دبورية</small><b>054-6111668</b></div>", "teal")

STORIES = [
    ("2026-10-27T19:30", "quiz-math-order", quiz("ميني درس · رياضيات", "شو الناتج؟<br><span style='direction:ltr;display:inline-block;font-family:Rubik;font-size:130px'>3 + 4 × 2</span>", ["14", "11", "10", "9"])),
    ("2026-10-27T21:20", "new-scroll", newpost("cov-scroll.jpg", "ريل جديد")),
    ("2026-10-28T13:00", "countdown-61", countdown(61)),
    ("2026-10-28T19:30", "ans-math-order", answer("الجواب", "3 + 4 × 2 = ?", "11", "الضرب قبل الجمع: <bdi dir=ltr>4 × 2 = 8</bdi>، وبعدين <bdi dir=ltr>3 + 8 = 11</bdi>.<br>أكثر غلطة بالامتحان: إنه نحسب بالترتيب من الشمال لليمين.", ltr=True)),
    ("2026-10-29T19:00", "tip-question", tip("بدل «درست؟»", "اسألوه: «شو أصعب سؤال لهلّأ؟»<br>الأول بيسكّر الحديث،<br>والثاني بيفتحه.")),
    ("2026-10-29T21:20", "new-five", newpost("cov-five.jpg", "تحدّي الخميس")),
    ("2026-10-30T13:00", "weekend-1", weekend("خطة نهاية الأسبوع", "ساعتين دراسة الصبح وهو مرتاح،<br>والتلفون برّا الغرفة وقتها.<br>والباقي إله، بلا ضغط.")),
    ("2026-10-31T19:30", "quiz-en-goes", quiz("Mini lesson · English", "She ___ to school<br>every day.", ["go", "goes", "going", "gone"], ltr=True)),
    ("2026-11-01T13:00", "ans-en-goes", answer("الجواب", "She ___ to school every day.", "goes", "مع he / she / it بالحاضر البسيط منضيف s للفعل:<br>She goes · He plays · It works", ltr=True)),
    ("2026-11-01T21:20", "new-crumpled", newpost("cov-crumpled.jpg", "منشور جديد")),
    ("2026-11-02T19:30", "poll-screen", poll("قديش ابنك بقعد<br>على التلفون باليوم؟", ["أقل من ساعتين", "من 2 لـ 4 ساعات", "أكثر من 4 ساعات"])),
    ("2026-11-03T13:00", "countdown-55", countdown(55)),
    ("2026-11-03T21:20", "new-chat", newpost("cov-chat.jpg", "ريل جديد")),
    ("2026-11-04T19:30", "quiz-ar-plural", quiz("ميني درس · عربي", "شو جمع كلمة<br>«كِتاب»؟", ["كُتُب", "كِتابات", "كاتِبون", "مَكتَبات"])),
    ("2026-11-05T13:00", "ans-ar-plural", answer("الجواب", "جمع كلمة «كِتاب»", "كُتُب", "جمع تكسير: الكلمة بتتغيّر من جوّا.<br>كاتِب ← كُتّاب · مَكتَبة ← مَكتَبات")),
    ("2026-11-06T13:00", "weekend-2", weekend("قبل الأسبوع الجاي", "اقعدوا معه 10 دقايق الجمعة<br>وشوفوا سوا: شو عنده امتحانات؟<br>وين محتاج مساعدة؟")),
]

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for when, slug, html in STORIES:
            pg.set_content(html, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(100)
            pg.screenshot(path=str(OUT / f"{when[:10]}-{slug}.png"))
        b.close()
    json.dump([[w, f"{w[:10]}-{s}.png"] for w, s, _ in STORIES], open(OUT / "schedule.json", "w"))
    print(len(STORIES))
