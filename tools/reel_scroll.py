"""Reel: السكرول المتجمّد — 1080x1920, 30fps, ~24s. Frames from a time-driven HTML page, then ffmpeg + synth SFX."""
import base64, pathlib, subprocess, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
NAME = sys.argv[1] if len(sys.argv) > 1 else "2026-10-27-scroll-freeze"
OUT = ROOT / "out" / NAME
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

FPS, DUR = 30, 24.0
T_FREEZE = 2.6

HTML = """<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>
""" + fonts + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Rubik;direction:rtl}
#feed{position:absolute;left:0;top:0;width:1080px}
.card{width:1080px;height:1920px;position:relative;overflow:hidden}
.card .shape{position:absolute;border-radius:50%}
.ui{position:absolute;left:40px;bottom:520px;display:flex;flex-direction:column;gap:56px}
.ui span{display:block;width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.85)}
.meta{position:absolute;right:50px;bottom:430px;left:200px}
.meta i{display:block;height:34px;border-radius:17px;background:rgba(255,255,255,.75);margin-top:20px}
.paper{background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px), #CFE0EE calc(100% - 3px));background-size:100% 80px}
.paper::before{content:"";position:absolute;top:0;bottom:0;right:150px;width:4px;background:#F2A7A7}
.hw{font-family:Marhey;color:#2B4C9B;font-weight:500}
#hook{position:absolute;top:300px;left:60px;right:60px;text-align:center}
.tag{display:inline-block;background:#fff;color:#14332F;font-weight:800;font-size:76px;line-height:1.25;padding:20px 40px;border-radius:26px;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.tag em{font-style:normal;background:#FFD84D;padding:0 12px;border-radius:10px}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
#scene2,#scene3,#scene4{position:absolute;inset:0;opacity:0}
.lines p{font-family:Marhey;color:#2B4C9B;font-size:66px;line-height:80px;font-weight:500}
.sticker{position:absolute;left:70px;right:70px;background:#22524E;color:#fff;border-radius:34px;padding:40px 48px;font-size:56px;line-height:1.45;font-weight:700;box-shadow:0 20px 40px rgba(0,0,0,.25)}
.sticker b{color:#FFD84D}
.note{position:absolute;right:190px;width:780px;padding:46px 50px 46px 60px;box-shadow:0 20px 34px rgba(0,0,0,.18)}
.note::before{content:"";position:absolute;top:-24px;left:50%;width:180px;height:50px;margin-left:-90px;background:rgba(255,255,255,.6);transform:rotate(-3deg)}
.note .n{font-family:Marhey;font-weight:700;font-size:70px;color:rgba(0,0,0,.2);position:absolute;top:24px;left:36px}
.note h3{font-family:Marhey;font-weight:700;font-size:64px;line-height:1.25;color:#1D2B3A}
.note p{font-size:44px;line-height:1.5;margin-top:14px;color:#26323A}
#scene4{background:#22524E;color:#fff;text-align:center}
.big{font-family:Marhey;font-weight:700;font-size:130px;line-height:1.15}
.yt{display:inline-block;background:#FFD84D;color:#14332F;padding:6px 40px 20px;border-radius:20px;transform:rotate(-3deg)}
</style></head><body>
<div id='feed'></div>
<div id='flash'></div>
<div id='scene2' class='paper'>
  <div class='lines' style='position:absolute;top:720px;right:200px;left:80px'>
    <p id='l1'>درس الرياضيات - صفحة 47</p>
    <p id='l2'>مساحة المثلث = القاعدة × الارتفاع ÷ 2</p>
    <p id='l3'>مثال: القاعدة 6 والارتفاع…</p>
  </div>
  <svg id='scrib' width='1080' height='1920' style='position:absolute;inset:0'><path id='sp' d='M800,1030 C640,990 540,1110 440,1050 C340,990 260,1130 170,1080' stroke='#E2574C' stroke-width='12' fill='none' stroke-linecap='round'/></svg>
  <div id='q' class='hw' style='position:absolute;top:1130px;right:200px;font-size:90px;font-weight:700;color:#E2574C;transform:rotate(-4deg)'>وين كنت؟</div>
  <div id='st1' class='sticker' style='top:1370px'>كل قفزة عالتلفون بتقطع حبل التركيز…<br><b>والرجعة للدفتر بدها وقت.</b></div>
</div>
<div id='scene3' class='paper'>
  <div class='hw' style='position:absolute;top:260px;right:190px;font-size:76px;font-weight:700;color:#24345E'>3 أشياء من الليلة</div>
  <svg width='1080' height='120' style='position:absolute;top:300px;left:0'><path d='M330,60 C500,48 700,70 900,52' stroke='#FFE36E' stroke-width='44' fill='none' stroke-linecap='round' opacity='.8'/></svg>
  <div id='n1' class='note' style='top:480px;background:#FFE98A'><div class='n'>1</div><h3>التلفون برّا الغرفة</h3><p>وقت الدراسة بس. مش عقاب، اتفاق.</p></div>
  <div id='n2' class='note' style='top:870px;background:#CDEBD9'><div class='n'>2</div><h3>خلّوه مكافأة</h3><p>25 دقيقة دراسة، وبعدها 5 دقايق التلفون إله.</p></div>
  <div id='n3' class='note' style='top:1260px;background:#FFD6BA'><div class='n'>3</div><h3>أول 10 دقايق معه</h3><p>البداية أصعب إشي. بعدها بيكمّل لحاله.</p></div>
</div>
<div id='scene4'>
  <img src='data:image/png;base64,""" + LOGO_W + """' style='height:120px;margin-top:330px'>
  <div class='big' style='margin-top:150px'>مش ضد التلفون.</div>
  <div class='big' style='margin-top:30px'><span class='yt'>مع ابنك.</span></div>
  <div style='font-size:50px;margin-top:150px;opacity:.95;line-height:1.5'>ابعتوا الفيديو لحدا لازم يشوفه</div>
  <div style='margin:60px auto 0;background:#fff;color:#22524E;border-radius:999px;width:760px;padding:26px 0'><div style='font-size:34px;color:#5E6E6B'>معهد رُوّاد · دبورية</div><div style='font-size:74px;font-weight:800;direction:ltr'>054-6111668</div></div>
</div>
<div id='hook'><div class='tag'>هاد اللي بصير براس ابنك<br><em>وهو بدرس</em></div></div>
<script>
const cols=[["#FF6B6B","#FFD93D"],["#6C5CE7","#00CEC9"],["#00B894","#FDCB6E"],["#E84393","#0984E3"],["#2D3436","#E17055"],["#FD79A8","#A29BFE"],["#55EFC4","#74B9FF"],["#FAB1A0","#6C5CE7"]];
const feed=document.getElementById('feed');
const N=8;
for(let i=0;i<N;i++){
  const c=document.createElement('div');c.className='card';
  if(i===N-1){c.classList.add('paper');c.innerHTML="<div class='hw' style='position:absolute;top:720px;right:200px;font-size:66px;line-height:80px'>درس الرياضيات - صفحة 47</div>";}
  else{
    const [a,b]=cols[i];
    c.style.background=`linear-gradient(${30+i*40}deg,${a},${b})`;
    c.innerHTML=`<div class='shape' style='width:${500+i*40}px;height:${500+i*40}px;left:${120+i*30}px;top:${520+(i%3)*90}px;background:rgba(255,255,255,.25)'></div>
      <div class='shape' style='width:220px;height:220px;right:${100+i*20}px;top:${360+i*40}px;background:rgba(0,0,0,.18)'></div>
      <div class='ui'><span></span><span></span><span></span></div><div class='meta'><i style='width:55%'></i><i style='width:85%'></i></div>`;
  }
  feed.appendChild(c);
}
const H=1920, D=(N-1)*H;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const outBack=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const pop=(el,t0,t)=>{const k=clamp((t-t0)/0.35);el.style.opacity=k>0?1:0;el.style.transform=`translateY(${(1-outBack(k))*120}px) rotate(${el.dataset.r||0}deg) scale(${0.85+0.15*outBack(k)})`;};
document.getElementById('n1').dataset.r=1.8;document.getElementById('n2').dataset.r=-2;document.getElementById('n3').dataset.r=1.4;
window.render=function(t){
  const F=""" + str(T_FREEZE) + """;
  // scene 1: scroll
  let y; if(t<F){y=D*ease(t/F);}else{y=D;}
  feed.style.transform=`translateY(${-y}px)`;
  const v=t<F?Math.abs(D*(ease(Math.min(1,(t+1/30)/F))-ease(t/F))):0;
  feed.style.filter=`blur(${Math.min(14,v/40)}px)`;
  // shake + flash at freeze
  const s=t>=F&&t<F+0.25?Math.sin((t-F)*90)*18*(1-(t-F)/0.25):0;
  feed.style.transform+=` translateX(${s}px)`;
  document.getElementById('flash').style.opacity=t>=F&&t<F+0.12?0.85*(1-(t-F)/0.12):0;
  // hook tag: visible 0..6.5
  const hook=document.getElementById('hook');
  hook.style.opacity=t<6.6?1:clamp(1-(t-6.6)/0.3);
  hook.style.transform=`scale(${t<0.3?0.9+0.1*outBack(t/0.3):1})`;
  // scene 2 notebook: 2.75..7.6
  const s2=document.getElementById('scene2');
  s2.style.opacity=t>=F+0.15&&t<7.6?1:(t>=7.6&&t<7.9?1-(t-7.6)/0.3:0);
  ['l1','l2','l3'].forEach((id,i)=>{document.getElementById(id).style.opacity=t>F+0.15+i*0.45?1:0;});
  const sp=document.getElementById('sp');const L=sp.getTotalLength();sp.style.strokeDasharray=L;sp.style.strokeDashoffset=L*(1-clamp((t-4.2)/0.5));
  const q=document.getElementById('q');q.style.opacity=t>4.5?1:0;q.style.transform=`rotate(-4deg) scale(${t>4.5?0.6+0.4*outBack(clamp((t-4.5)/0.3)):0.6})`;
  pop(document.getElementById('st1'),5.1,t);
  // scene 3 notes: 7.6..19
  const s3=document.getElementById('scene3');
  s3.style.opacity=t>=7.6&&t<19?clamp((t-7.6)/0.3):(t>=19&&t<19.3?1-(t-19)/0.3:0);
  pop(document.getElementById('n1'),8.2,t);pop(document.getElementById('n2'),11.6,t);pop(document.getElementById('n3'),15.0,t);
  // scene 4 end card 19..
  const s4=document.getElementById('scene4');
  s4.style.opacity=t>=19?clamp((t-19)/0.3):0;
};
</script></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    n = int(DUR * FPS)
    for i in range(n):
        pg.evaluate(f"render({i/FPS})")
        pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=92)
    b.close()

# --- synth SFX ---
A = OUT / "sfx.wav"
filt = (
    "anoisesrc=d=2.6:c=pink:a=0.5,highpass=f=500,lowpass=f=4000,afade=t=in:d=1.8,afade=t=out:st=2.4:d=0.2,volume=0.55[w];"
    "sine=f=80:d=0.35,afade=t=out:d=0.35,volume=1.6,adelay=2600|2600[th];"
    "sine=f=880:d=0.15,afade=t=out:d=0.15,volume=0.5,adelay=4500|4500[q];"
    "sine=f=660:d=0.12,afade=t=out:d=0.12,volume=0.45,adelay=5100|5100[p0];"
    "sine=f=700:d=0.12,afade=t=out:d=0.12,volume=0.5,adelay=8200|8200[p1];"
    "sine=f=790:d=0.12,afade=t=out:d=0.12,volume=0.5,adelay=11600|11600[p2];"
    "sine=f=880:d=0.12,afade=t=out:d=0.12,volume=0.5,adelay=15000|15000[p3];"
    "sine=f=523:d=1.2,afade=t=out:d=1.2,volume=0.35,adelay=19000|19000[c1];"
    "sine=f=659:d=1.2,afade=t=out:d=1.2,volume=0.3,adelay=19080|19080[c2];"
    "sine=f=784:d=1.4,afade=t=out:d=1.4,volume=0.3,adelay=19160|19160[c3];"
    "[w][th][q][p0][p1][p2][p3][c1][c2][c3]amix=inputs=10:normalize=0,apad=whole_dur=24,atrim=0:24"
)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
MP4 = OUT / "reel.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(MP4)], check=True)
print(MP4)
