"""Reel: 5 ثواني — a grade-8 equation with a 5-second countdown, then the worked solution. 1080x1920, 30fps, 15.5s."""
import base64, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out" / "2026-10-29-five-seconds"
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
FPS, DUR = 30, 15.5

HTML = """<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>""" + fonts + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Rubik;direction:rtl}
.paper{position:absolute;inset:0;background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px), #CFE0EE calc(100% - 3px));background-size:100% 80px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:120px;width:4px;background:#F2A7A7}
#hook{position:absolute;top:270px;left:60px;right:60px;text-align:center}
.tag{display:inline-block;background:#22524E;color:#fff;font-weight:800;font-size:68px;line-height:1.3;padding:22px 42px;border-radius:28px;box-shadow:0 16px 36px rgba(0,0,0,.2)}
.tag em{font-style:normal;color:#14332F;background:#FFD84D;padding:0 14px;border-radius:12px}
#eq{position:absolute;top:640px;left:90px;right:90px;background:#fff;border-radius:40px;box-shadow:0 20px 50px rgba(0,0,0,.12);padding:50px 0;text-align:center}
#eq .e{font-weight:800;font-size:150px;color:#1A2B29;direction:ltr;letter-spacing:4px}
#eq .x{font-family:Marhey;font-size:74px;color:#2B4C9B;margin-top:6px}
#timer{position:absolute;top:1080px;left:50%;margin-left:-170px;width:340px;height:340px}
#tn{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:170px;color:#E2574C;direction:ltr}
#sol{position:absolute;top:1080px;left:120px;right:180px;opacity:0}
#sol p{font-family:Marhey;color:#2B4C9B;font-size:84px;line-height:110px;direction:ltr;text-align:right;font-weight:500}
#ans{position:relative;display:inline-block;color:#E2574C!important;font-weight:700!important;font-size:120px!important}
#ask{position:absolute;top:1590px;left:80px;right:80px;background:#FFE98A;padding:34px 40px;font-size:50px;line-height:1.45;font-weight:700;color:#1D2B3A;box-shadow:0 18px 30px rgba(0,0,0,.15);transform:rotate(-1.5deg);opacity:0;text-align:center}
#end{position:absolute;inset:0;background:#22524E;color:#fff;text-align:center;opacity:0}
.big{font-family:Marhey;font-weight:700;font-size:120px;line-height:1.2}
.yt{display:inline-block;background:#FFD84D;color:#14332F;padding:6px 40px 20px;border-radius:20px;transform:rotate(-3deg)}
</style></head><body>
<div class='paper'></div>
<div id='hook'><div class='tag'>ابنك بالصف الثامن…<br>بيحلّها <em>بـ5 ثواني؟</em></div></div>
<div id='eq'><div class='e'>3x + 7 = 22</div><div class='x'>شو قيمة x؟</div></div>
<div id='timer'><svg width='340' height='340'><circle cx='170' cy='170' r='150' stroke='#F2E6D0' stroke-width='22' fill='#fff'/><circle id='ring' cx='170' cy='170' r='150' stroke='#E2574C' stroke-width='22' fill='none' stroke-linecap='round' transform='rotate(-90 170 170)'/></svg><div id='tn'>5</div></div>
<div id='sol'>
 <p id='s1'>3x = 22 − 7 = 15</p>
 <p id='s2'>x = 15 ÷ 3</p>
 <p id='s3'><span id='ans'>x = 5<svg width='330' height='170' style='position:absolute;left:-60px;top:-10px;overflow:visible'><ellipse id='circ' cx='170' cy='80' rx='190' ry='78' stroke='#E2574C' stroke-width='9' fill='none' transform='rotate(-4 170 80)'/></svg></span></p>
</div>
<div id='ask'>حلّها بـ5 ثواني؟<br>اكتبولنا بالتعليقات: آه ولا علق؟</div>
<div id='end'>
  <img src='data:image/png;base64,""" + LOGO_W + """' style='height:120px;margin-top:380px'>
  <div class='big' style='margin-top:150px'>إذا علق…</div>
  <div class='big' style='margin-top:30px'><span class='yt'>مش لحاله.</span></div>
  <div style='font-size:50px;margin-top:130px;line-height:1.5'>دروس تقوية بالرياضيات لكل الصفوف</div>
  <div style='margin:60px auto 0;background:#fff;color:#22524E;border-radius:999px;width:760px;padding:26px 0'><div style='font-size:34px;color:#5E6E6B'>معهد رُوّاد · دبورية</div><div style='font-size:74px;font-weight:800;direction:ltr'>054-6111668</div></div>
</div>
<script>
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const outBack=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const ring=document.getElementById('ring');const C=2*Math.PI*150;ring.style.strokeDasharray=C;
const circ=document.getElementById('circ');const CL=circ.getTotalLength?circ.getTotalLength():1200;circ.style.strokeDasharray=CL;
window.render=function(t){
  const T0=0.6,T1=5.6;
  const k=clamp((t-T0)/(T1-T0));
  ring.style.strokeDashoffset=C*k;
  const n=t<T0?5:Math.max(0,5-Math.floor((t-T0)));
  document.getElementById('tn').textContent=n;
  const ph=(t-T0)%1;document.getElementById('tn').style.transform=`scale(${t>=T0&&t<T1?1+0.18*Math.max(0,1-ph*4):1})`;
  const tm=document.getElementById('timer');tm.style.opacity=t<T1?1:clamp(1-(t-T1)/0.2);
  const sol=document.getElementById('sol');sol.style.opacity=t>=T1?1:0;
  document.getElementById('s1').style.opacity=t>5.8?1:0;
  document.getElementById('s2').style.opacity=t>6.6?1:0;
  const a=document.getElementById('s3');a.style.opacity=t>7.4?1:0;
  document.getElementById('ans').style.transform=`scale(${t>7.4?0.6+0.4*outBack(clamp((t-7.4)/0.3)):0.6})`;
  circ.style.strokeDashoffset=CL*(1-clamp((t-7.8)/0.45));
  const ask=document.getElementById('ask');const ak=clamp((t-8.6)/0.35);ask.style.opacity=ak>0?1:0;ask.style.transform=`rotate(-1.5deg) translateY(${(1-outBack(ak))*120}px)`;
  document.getElementById('end').style.opacity=t>=12?clamp((t-12)/0.3):0;
  document.getElementById('hook').style.transform=`scale(${t<0.3?0.9+0.1*outBack(t/0.3):1})`;
};
</script></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load")
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})")
        pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=92)
    b.close()

ticks = "".join(f"sine=f={1000 if s<4 else 1400}:d=0.06,afade=t=out:d=0.06,volume=0.5,adelay={600+s*1000}|{600+s*1000}[t{s}];" for s in range(5))
filt = (ticks +
    "sine=f=523:d=0.25,afade=t=out:d=0.25,volume=0.5,adelay=5600|5600[b1];sine=f=392:d=0.35,afade=t=out:d=0.35,volume=0.5,adelay=5800|5800[b2];"
    "sine=f=660:d=0.12,afade=t=out:d=0.12,volume=0.4,adelay=5800|5800[w1];sine=f=700:d=0.12,afade=t=out:d=0.12,volume=0.4,adelay=6600|6600[w2];"
    "sine=f=1046:d=0.5,afade=t=out:d=0.5,volume=0.4,adelay=7400|7400[g1];sine=f=1318:d=0.6,afade=t=out:d=0.6,volume=0.3,adelay=7500|7500[g2];"
    "sine=f=790:d=0.12,afade=t=out:d=0.12,volume=0.45,adelay=8600|8600[p];"
    "sine=f=523:d=1.2,afade=t=out:d=1.2,volume=0.35,adelay=12000|12000[c1];sine=f=659:d=1.2,afade=t=out:d=1.2,volume=0.3,adelay=12080|12080[c2];sine=f=784:d=1.4,afade=t=out:d=1.4,volume=0.3,adelay=12160|12160[c3];"
    "[t0][t1][t2][t3][t4][b1][b2][w1][w2][g1][g2][p][c1][c2][c3]amix=inputs=15:normalize=0,apad=whole_dur=15.5,atrim=0:15.5")
A = OUT / "sfx.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
MP4 = OUT / "reel.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(MP4)], check=True)
print(MP4)
