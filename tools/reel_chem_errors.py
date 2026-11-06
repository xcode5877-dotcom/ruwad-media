"""Reel: 3 أخطاء بتضيّع علامات بالكيمياء — الصف التاسع. 1080x1920, 30fps, 12s.
Hook is on screen from frame 0; each mistake: wrong line, red pen strike, correct line."""
import base64, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "2026-11-08-chem-errors"
FR = OUT / "frames"
shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
NM = ROOT / "node_modules/@fontsource"
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
fonts = ""
for fam, pkg, ws in (("Rubik", "rubik", (500, 700, 800)), ("Marhey", "marhey", (500, 700))):
    for w in ws:
        for sub in ("arabic", "latin"):
            f = NM / pkg / "files" / f"{pkg}-{sub}-{w}-normal.woff2"
            if f.exists():
                fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"
LOGO_W = b64(ROOT / "logo-white.png")
FPS, DUR = 30, 12.0
# each mistake: (start, wrong html, right html)
ITEMS = [
    (0.5, "<span class='f'>2H = H<sub>2</sub></span>",
          "<span class='f'>2H</span> = ذرّتين لحال<br><span class='f'>H<sub>2</sub></span> = جزيء واحد"),
    (3.6, "<span class='f'>2H<sub>2</sub> + O<sub>2</sub> → H<sub>2</sub>O</span>",
          "<span class='f'>2H<sub>2</sub> + O<sub>2</sub> → <u>2</u>H<sub>2</sub>O</span><br>المعامل جزء من الجواب"),
    (6.7, "<span class='f'>Na</span>: فيها 23 بروتون",
          "<span class='f'>Z = 11</span> بروتونات<br><span class='f'>A = 23</span> = 11 + 12 نيوترون"),
]
WRONG_T = ["الغلطة الأولى", "الغلطة الثانية", "الغلطة الثالثة"]

cards = ""
for i, (_, w, r) in enumerate(ITEMS):
    cards += f"""<div class='card' id='c{i}'>
  <div class='num'>{WRONG_T[i]}</div>
  <div class='wrong' id='w{i}'><b class='mk x'>✗</b><div class='t'>{w}
    <svg class='strike' viewBox='0 0 100 60' preserveAspectRatio='none'><path id='p{i}' d='M100 34 C 75 20, 40 44, 0 28' stroke='#E2574C' stroke-width='12' fill='none' stroke-linecap='round' vector-effect='non-scaling-stroke'/></svg></div></div>
  <div class='right' id='r{i}'><b class='mk v'>✓</b><div class='t'>{r}</div></div>
</div>"""

HTML = """<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>""" + fonts + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Rubik;direction:rtl;color:#1A2B29}
.paper{position:absolute;inset:0;background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px), #CFE0EE calc(100% - 3px));background-size:100% 80px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:120px;width:4px;background:#F2A7A7}
#hook{position:absolute;top:250px;left:60px;right:60px;text-align:center}
.chip{display:inline-block;background:#E2574C;color:#fff;font-weight:800;font-size:46px;padding:12px 34px;border-radius:999px;margin-bottom:26px}
.tag{display:block;background:#22524E;color:#fff;font-weight:800;font-size:82px;line-height:1.25;padding:30px 30px;border-radius:30px;box-shadow:0 16px 36px rgba(0,0,0,.2)}
.tag em{font-style:normal;color:#14332F;background:#FFD84D;padding:0 16px;border-radius:14px}
#dots{position:absolute;top:760px;left:0;right:0;display:flex;justify-content:center;gap:22px}
#dots i{width:26px;height:26px;border-radius:50%;background:#D8D2C2}
.card{position:absolute;top:830px;left:70px;right:150px;opacity:0}
.num{font-family:Marhey;font-weight:700;font-size:62px;color:#E2574C;margin-bottom:24px}
.wrong,.right{position:relative;display:flex;gap:28px;align-items:center;background:#fff;border-radius:30px;padding:30px 34px;box-shadow:0 12px 30px rgba(0,0,0,.10)}
.wrong{border:5px solid #F3C2BD}
.right{margin-top:40px;border:6px solid #2E9B6A;background:#EFF9F3;opacity:0}
.mk{flex:none;width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:62px;font-weight:800}
.x{background:#E2574C}.v{background:#2E9B6A}
.t{font-size:62px;font-weight:700;line-height:1.35}
.wrong .t{color:#7A6A68}
.f{direction:ltr;unicode-bidi:isolate;display:inline-block;font-weight:800;color:#24345E}
.wrong .f{color:#7A6A68}
sub{font-size:.6em;vertical-align:-.25em}
u{text-decoration:none;color:#fff;background:#2E9B6A;border-radius:10px;padding:0 10px}
.t{position:relative}.strike{position:absolute;right:-10px;left:-10px;width:calc(100% + 20px);height:60px;top:50%;margin-top:-30px;overflow:visible}
#stage{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
#save{position:absolute;bottom:250px;left:90px;right:150px;text-align:center;background:#FFE98A;padding:28px 30px;font-family:Marhey;font-weight:700;font-size:60px;color:#1D2B3A;transform:rotate(-1.5deg);box-shadow:0 18px 30px rgba(0,0,0,.15);opacity:0}
#end{position:absolute;inset:0;background:#22524E;color:#fff;text-align:center;opacity:0}
.big{font-family:Marhey;font-weight:700;font-size:112px;line-height:1.2}
.yt{display:inline-block;background:#FFD84D;color:#14332F;padding:6px 40px 20px;border-radius:20px;transform:rotate(-3deg)}
</style></head><body>
<div id='stage'><div class='paper'></div>
<div id='hook'><div class='chip'>الصف التاسع · كيمياء</div><div class='tag'>3 أخطاء بتضيّع<br><em>علامات بالكيمياء</em> ❌</div></div>
<div id='dots'><i></i><i></i><i></i></div>
""" + cards + """
<div id='save'>احفظوه لليلة الامتحان 🔖</div>
<div id='end'>
  <img src='data:image/png;base64,""" + LOGO_W + """' style='height:120px;margin-top:400px'>
  <div class='big' style='margin-top:140px'>وقعت بوحدة منهم؟</div>
  <div class='big' style='margin-top:30px'><span class='yt'>علّق 🔥</span></div>
  <div style='font-size:50px;margin-top:120px;line-height:1.5'>دروس تحضير للتاسع<br>وامتحانات تجريبية على منصة رواد</div>
  <div style='margin:60px auto 0;background:#fff;color:#22524E;border-radius:999px;width:760px;padding:26px 0'><div style='font-size:34px;color:#5E6E6B'>معهد رُوّاد · دبورية</div><div style='font-size:74px;font-weight:800;direction:ltr'>054-6111668</div></div>
</div></div>
<script>
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const outBack=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const S=[""" + ",".join(str(s) for s, _, _ in ITEMS) + """];const L=3.1;
const P=S.map((_,i)=>{const p=document.getElementById('p'+i);const n=p.getTotalLength();p.style.strokeDasharray=n;return [p,n];});
const dots=[...document.querySelectorAll('#dots i')];
window.render=function(t){
  document.getElementById('hook').style.transform=`scale(${t<0.25?0.94+0.06*outBack(t/0.25):1})`;
  S.forEach((s,i)=>{
    const c=document.getElementById('c'+i);const lt=t-s;
    const vis=lt>=0&&lt<L;const ent=clamp(lt/0.25);
    c.style.opacity=vis?ent:0;c.style.transform=`translateX(${(1-outBack(ent))*-120}px)`;
    const [p,n]=P[i];p.style.strokeDashoffset=n*(1-clamp((lt-0.7)/0.3));
    const r=document.getElementById('r'+i);const rk=clamp((lt-1.15)/0.25);
    r.style.opacity=rk;r.style.transform=`scale(${0.85+0.15*outBack(rk)})`;
    dots[i].style.background=t>=s?(t<s+L?'#E2574C':'#2E9B6A'):'#D8D2C2';
    dots[i].style.transform=`scale(${vis?1.35:1})`;
  });
  const sv=document.getElementById('save');const sk=clamp((t-9.4)/0.3);sv.style.opacity=sk;sv.style.transform=`rotate(-1.5deg) translateY(${(1-outBack(sk))*100}px)`;
  if(t>=9.8){S.forEach((_,i)=>{});}
  document.getElementById('end').style.opacity=t>=10.3?clamp((t-10.3)/0.3):0;
};
</script></body></html>"""

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(HTML, wait_until="load")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        for i in range(int(DUR * FPS)):
            pg.evaluate(f"render({i/FPS})")
            pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=92)
        b.close()
    # sfx: pop on each card, scratch on each strike, ding on each correct, chord at end
    parts, labels = [], []
    for k, (s, _, _) in enumerate(ITEMS):
        ms = int(s * 1000)
        parts += [f"sine=f=660:d=0.1,afade=t=out:d=0.1,volume=0.45,adelay={ms}|{ms}[a{k}];",
                  f"anoisesrc=d=0.3:c=pink:a=0.35,bandpass=f=2500:w=1800,afade=t=in:d=0.05,afade=t=out:st=0.2:d=0.1,adelay={ms+700}|{ms+700}[n{k}];",
                  f"sine=f=1046:d=0.45,afade=t=out:d=0.45,volume=0.4,adelay={ms+1150}|{ms+1150}[d{k}];",
                  f"sine=f=1318:d=0.5,afade=t=out:d=0.5,volume=0.28,adelay={ms+1230}|{ms+1230}[e{k}];"]
        labels += [f"[a{k}]", f"[n{k}]", f"[d{k}]", f"[e{k}]"]
    parts += ["sine=f=790:d=0.12,afade=t=out:d=0.12,volume=0.45,adelay=9400|9400[s];",
              "sine=f=523:d=1.3,afade=t=out:d=1.3,volume=0.35,adelay=10300|10300[c1];sine=f=659:d=1.3,afade=t=out:d=1.3,volume=0.3,adelay=10380|10380[c2];sine=f=784:d=1.5,afade=t=out:d=1.5,volume=0.3,adelay=10460|10460[c3];"]
    labels += ["[s]", "[c1]", "[c2]", "[c3]"]
    filt = "".join(parts) + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR}"
    A = OUT / "sfx.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
    MP4 = OUT / "reel.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", str(MP4)], check=True)
    print(MP4)
