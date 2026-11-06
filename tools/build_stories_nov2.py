"""Stories 6–8 Nov 2026 (approved 5.11). Reuses the style helpers of build_stories.py. 1080x1920 PNG."""
import base64, pathlib, subprocess
from playwright.sync_api import sync_playwright
# load only the style helpers of build_stories.py (its module-level STORIES list needs old cover files)
_src = (pathlib.Path(__file__).parent / "build_stories.py").read_text(encoding="utf-8").split("\nSTORIES = [")[0]
_ns = {"__file__": str(pathlib.Path(__file__).parent / "build_stories.py")}; exec(_src, _ns)
page, quiz, countdown, LT, LW, b64, OUT = (_ns[k] for k in ("page", "quiz", "countdown", "LT", "LW", "b64", "OUT"))

ROOT = pathlib.Path(__file__).parent
REPO = ROOT.parent

def exam_countdown(n):
    return page(LW + "<div style='position:absolute;top:400px;left:0;right:0;text-align:center'>"
                + f"<div style='font-weight:800;font-size:330px;line-height:1;direction:ltr'>{n}</div>"
                + "<div class='hand' style='font-size:90px;font-weight:700;margin-top:6px'>يوم لـ 26/11</div>"
                + "<div style='margin-top:30px'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:54px'>الامتحانات الفصلية · سابع ثامن تاسع</span></div></div>"
                + "<div class='sticky' style='top:1080px;right:150px;left:110px;background:#CDEBD9;transform:rotate(-1.5deg);color:#1A2B29;padding:40px 50px'>"
                + "<div style='font-size:42px;font-weight:700;color:#22524E'>جواب امبارح</div>"
                + "<div style='font-size:56px;font-weight:800;margin-top:10px'>5 ذرّات<div style='direction:ltr;font-size:52px;margin-top:8px;letter-spacing:2px'>Ca + O + O + H + H</div></div></div>"
                + "<div class='wa' style='bottom:340px'><small>بدكم خطة لابنكم؟ ابعتولنا الصف والمادة</small><b>054-6111668</b></div>", "teal")

def share_poll(cover, label, q, opts):
    o = "".join(f"<div style='background:#fff;color:#22524E;border-radius:22px;padding:14px 30px;font-size:44px;font-weight:700'>{t}</div>" for t in opts)
    return page(LW + f"<div style='position:absolute;top:380px;left:0;right:0;text-align:center'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:52px'>{label}</span></div>"
                + f"<img src='data:image/png;base64,{b64(cover)}' style='position:absolute;top:500px;left:50%;width:440px;margin-left:-220px;border-radius:30px;border:10px solid #fff;transform:rotate(-3deg);box-shadow:0 30px 60px rgba(0,0,0,.45)'>"
                + f"<div class='hand' style='position:absolute;top:1120px;left:0;right:0;text-align:center;font-size:64px;font-weight:700'>{q}</div>"
                + f"<div style='position:absolute;top:1240px;left:160px;right:160px;display:flex;flex-direction:column;gap:18px;text-align:center'>{o}</div>"
                + "<div style='position:absolute;bottom:300px;left:0;right:0;text-align:center;font-size:40px;opacity:.9'>ردّوا على الستوري 👇</div>", "teal")

def share_reel(cover, label, line):
    return page(LW + f"<div style='position:absolute;top:400px;left:0;right:0;text-align:center'><span class='chip' style='background:#FFD84D;color:#14332F;font-size:56px'>{label}</span></div>"
                + f"<img src='data:image/jpeg;base64,{b64(cover)}' style='position:absolute;top:530px;left:50%;width:470px;margin-left:-235px;border-radius:34px;border:10px solid #fff;transform:rotate(-3deg);box-shadow:0 30px 60px rgba(0,0,0,.45)'>"
                + f"<div class='hand' style='position:absolute;bottom:370px;left:60px;right:60px;text-align:center;font-size:62px;font-weight:700;line-height:1.35'>{line}</div>", "teal")

REEL_COVER = ROOT / "out" / "2026-11-08-chem-errors" / "cover.jpg"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2.0", "-i", str(ROOT / "out/2026-11-08-chem-errors/reel.mp4"),
                "-frames:v", "1", "-q:v", "3", str(REEL_COVER)], check=True)
CAROUSEL_COVER = sorted((REPO / "posts" / "2026-11-07-three-week-plan").glob("*.png"))[0]

STORIES = [
    ("2026-11-06T19:30", "quiz-chem-atoms", quiz("تحدّي التاسع · 5 ثواني ⏱",
        "كم ذرّة بـ<br><span style='direction:ltr;display:inline-block;font-family:Rubik;font-size:140px'>Ca(OH)<sub style='font-size:.55em'>2</sub></span> ؟", ["3", "4", "5"])),
    ("2026-11-07T13:00", "cd-exams-19", exam_countdown(19)),
    ("2026-11-07T21:00", "new-plan-poll", share_poll(CAROUSEL_COVER, "منشور جديد", "ابنك بأي أسبوع؟", ["🗺️ الخريطة", "✍️ التدريب", "لسا ما بلّش"])),
    ("2026-11-08T13:00", "countdown-50", countdown(50)),
    ("2026-11-08T19:30", "new-chem-reel", share_reel(REEL_COVER, "ريل جديد", "وقعت بوحدة منهم؟<br>علّق 🔥 عالريل")),
]

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for when, slug, html in STORIES:
            pg.set_content(html, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / f"{when[:10]}-{slug}.png"))
            print(f"{when[:10]}-{slug}.png")
        b.close()
