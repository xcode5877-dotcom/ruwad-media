"""Reel 2026-11-03: رسالة من ابنك — a WhatsApp chat typed live, then the parent's reply. 1080x1920, 30fps, 23s."""
import base64, json, os, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
TRIAL = os.environ.get("TRIAL") == "1"
OFF = 2.2 if TRIAL else 0.0
OUT = ROOT / "out" / ("2026-11-04-chat-trial" if TRIAL else "2026-11-03-chat")
FR = OUT / "frames"
shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
NM = ROOT / "node_modules/@fontsource"
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
fonts = ""
for fam, pkg, ws in (("Rubik", "rubik", (400, 500, 700, 800)), ("Marhey", "marhey", (500, 700))):
    for w in ws:
        for sub in ("arabic", "latin"):
            f = NM / pkg / "files" / f"{pkg}-{sub}-{w}-normal.woff2"
            if f.exists():
                fonts += f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}\n"
LOGO_W = b64(ROOT / "logo-white.png")
FPS, DUR = 30, 23.0 + OFF

INTRO = """<div id='intro' style='position:absolute;inset:0;background-color:#FFFDF6;background-image:linear-gradient(transparent 0 calc(100% - 3px),#CFE0EE calc(100% - 3px));background-size:100% 90px;display:block'>
<div style='position:absolute;top:0;bottom:0;right:150px;width:4px;background:#F2A7A7'></div>
<div style='position:absolute;top:700px;right:200px;font-family:Marhey;font-size:120px;color:#2B4C9B;font-weight:700'>ابني <span id='w1' style='position:relative;color:#7E8FB8'>كسلان<svg viewBox='0 0 400 100' preserveAspectRatio='none' style='position:absolute;left:-20px;top:40px;width:calc(100% + 40px);height:70px;overflow:visible'><path id='sk' d='M5,60 C100,40 200,75 395,45' stroke='#E2574C' stroke-width='16' fill='none' stroke-linecap='round'/></svg></span></div>
<div id='w2' style='position:absolute;top:900px;right:360px;font-family:Marhey;font-size:130px;color:#E2574C;font-weight:700;transform:rotate(-5deg);opacity:0'>تعبان.</div>
</div>"""
# (who, text, typing_start, appear_time, clock)
MSGS = [
    ("son", "يمّا، بكرا عندي امتحان", 0.35, 1.3, "21:04"),
    ("son", "بقعد أدرس… وبعد 5 دقايق بلاقي حالي عالتلفون", 1.8, 3.4, "21:04"),
    ("son", "مش قصدي. والله بدي أنجح", 3.9, 5.1, "21:05"),
    ("son", "بس راسي مليان ضجة", 5.6, 6.6, "21:05"),
    ("son", "ساعدوني… بس بدون صريخ", 7.1, 8.3, "21:06"),
    ("me", "تعال نحط التلفون برّا، وأنا بقعد معك أول 10 دقايق.", 11.0, 14.6, "21:07"),
    ("son", "ماشي يمّا ♥", 15.4, 16.6, "21:07"),
]
REPLY_TYPE = (11.0, 14.2)  # parent types in the input bar

HTML = """<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>""" + fonts + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Rubik;direction:rtl}
#bg{position:absolute;inset:0;background:#EFE7DB}
#bar{position:absolute;top:0;left:0;right:0;height:250px;background:#22524E;color:#fff;display:flex;align-items:flex-end;gap:30px;padding:0 60px 40px}
.av{width:110px;height:110px;border-radius:50%;background:#F0A04B;display:flex;align-items:center;justify-content:center;font-family:Marhey;font-weight:700;font-size:56px}
#bar b{display:block;font-size:52px}#st{font-size:36px;opacity:.85}
#msgs{position:absolute;top:250px;bottom:420px;left:50px;right:50px;padding-top:20px;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;gap:22px}
.m{max-width:820px;padding:28px 38px 18px;font-size:52px;line-height:1.38;border-radius:38px;box-shadow:0 3px 0 rgba(0,0,0,.07);transform-origin:top right}
.son{align-self:flex-start;background:#fff;border-top-right-radius:10px}
.me{align-self:flex-end;background:#D3F3C4;border-top-left-radius:10px;transform-origin:top left}
.m i{display:block;font-style:normal;font-size:28px;color:#7A8784;text-align:left;margin-top:4px;direction:ltr}
.tick{color:#3BA0E6;font-weight:700}
.typing{align-self:flex-start;background:#fff;border-radius:38px;padding:30px 40px;display:flex;gap:14px}
.typing span{width:20px;height:20px;border-radius:50%;background:#9AA5A3}
#input{position:absolute;bottom:250px;left:40px;right:40px;height:130px;background:#fff;border-radius:65px;display:flex;align-items:center;padding:0 50px;font-size:46px;color:#9AA5A3;box-shadow:0 4px 10px rgba(0,0,0,.08)}
#input.on{color:#1A2B29}
#caret{display:inline-block;width:4px;height:52px;background:#22524E;margin-right:4px;vertical-align:middle}
#hook{position:absolute;top:300px;left:60px;right:60px;text-align:center}
.tag{display:inline-block;background:#FFD84D;color:#14332F;font-weight:800;font-size:70px;line-height:1.28;padding:22px 44px;border-radius:26px;box-shadow:0 16px 36px rgba(0,0,0,.2);transform:rotate(-2deg)}
#ask{position:absolute;top:300px;left:60px;right:60px;text-align:center;opacity:0}
#ask div{display:inline-block;background:#22524E;color:#fff;font-family:Marhey;font-weight:700;font-size:76px;padding:20px 50px 34px;border-radius:24px;transform:rotate(2deg);box-shadow:0 16px 36px rgba(0,0,0,.25)}
#end{position:absolute;inset:0;background:#22524E;color:#fff;text-align:center;opacity:0}
.big{font-family:Marhey;font-weight:700;font-size:100px;line-height:1.3}
.yt{display:inline-block;background:#FFD84D;color:#14332F;padding:4px 36px 18px;border-radius:20px;transform:rotate(-3deg)}
</style></head><body>
<div id='bg'></div>
<div id='bar'><div class='av'>ا</div><div><b>ابني</b><span id='st'>متصل الآن</span></div></div>
<div id='msgs'></div>
<div id='input'><span id='itext'>اكتب رسالة</span><span id='caret' style='opacity:0'></span></div>
<div id='hook'><div class='tag'>لو ابنك بيحكيلك<br>شو بصير معه بالامتحانات…</div></div>
<div id='ask'><div>شو رح تجاوبوه؟</div></div>
<div id='end'>
  <img src='data:image/png;base64,""" + LOGO_W + """' style='height:120px;margin-top:360px'>
  <div class='big' style='margin-top:140px'>مرات كل اللي بدّه إياه…</div>
  <div class='big' style='margin-top:30px'><span class='yt'>حدا يقعد جنبه.</span></div>
  <div style='font-size:48px;margin-top:120px;line-height:1.5'>ابعتوا الفيديو لأم أو أب لازم يشوفوه</div>
  <div style='margin:56px auto 0;background:#fff;color:#22524E;border-radius:999px;width:760px;padding:26px 0'><div style='font-size:34px;color:#5E6E6B'>معهد رُوّاد · دبورية</div><div style='font-size:74px;font-weight:800;direction:ltr'>054-6111668</div></div>
</div>
__INTRO__<script>
const MSGS=__MSGS__; const RT=__RT__;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const outBack=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const box=document.getElementById('msgs');
window.render=function(T){const OFF=__OFF__;const t=Math.max(0,T-OFF);const IN=document.getElementById('intro');if(IN){IN.style.opacity=T<OFF?1:clamp(1-(T-OFF)/0.2);const sk=document.getElementById('sk');const L=sk.getTotalLength();sk.style.strokeDasharray=L;sk.style.strokeDashoffset=L*(1-clamp((T-0.25)/0.4));const w2=document.getElementById('w2');w2.style.opacity=T>0.9?1:0;w2.style.transform=`rotate(-5deg) scale(${T>0.9?0.6+0.4*outBack(clamp((T-0.9)/0.3)):0.6})`;}if(T<OFF){}
  let html='';let typing=false;
  for(const [who,txt,ts,ta,clk] of MSGS){
    if(t>=ta){
      const k=clamp((t-ta)/0.22);const sc=0.6+0.4*outBack(k);
      const tick=who==='me'?" <span class='tick'>✓✓</span>":"";
      html+=`<div class='m ${who}' style='transform:scale(${sc});opacity:${k>0?1:0}'>${txt}<i>${clk}${tick}</i></div>`;
    } else if(who==='son' && t>=ts){ typing=true;
      const ph=t*6;
      html+=`<div class='typing'>${[0,1,2].map(i=>`<span style='transform:translateY(${-10*Math.max(0,Math.sin(ph-i*0.9))}px)'></span>`).join('')}</div>`;
    }
  }
  box.innerHTML=html;
  document.getElementById('st').textContent=typing?'يكتب…':'متصل الآن';
  // parent types in the input bar
  const it=document.getElementById('itext'),inp=document.getElementById('input'),car=document.getElementById('caret');
  const reply=MSGS[5][1];
  if(t>=RT[0]&&t<MSGS[5][3]){const n=Math.floor(reply.length*clamp((t-RT[0])/(RT[1]-RT[0])));it.textContent=reply.slice(0,n);inp.classList.add('on');car.style.opacity=(Math.floor(t*3)%2)?1:0;}
  else{it.textContent='اكتب رسالة';inp.classList.remove('on');car.style.opacity=0;}
  document.getElementById('hook').style.opacity=t<4.6?1:clamp(1-(t-4.6)/0.3);
  document.getElementById('hook').style.transform=`scale(${t<0.3?0.9+0.1*outBack(t/0.3):1})`;
  const ak=document.getElementById('ask');const a=t>=8.9&&t<11.2;ak.style.opacity=a?1:(t>=11.2&&t<11.5?1-(t-11.2)/0.3:0);
  ak.style.transform=`scale(${t>=8.9?0.7+0.3*outBack(clamp((t-8.9)/0.3)):0.7})`;
  document.getElementById('end').style.opacity=t>=18?clamp((t-18)/0.3):0;
};
</script></body></html>"""
HTML = HTML.replace("__INTRO__", (INTRO if TRIAL else "")).replace("__OFF__", str(OFF)).replace("__MSGS__", json.dumps(MSGS, ensure_ascii=False)).replace("__RT__", json.dumps(REPLY_TYPE))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})")
        pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=92)
    b.close()

# SFX: pop per received message, whoosh on send, soft key clicks while the parent types, end chord
parts, labels = [], []
def add(expr, ms):
    ms = int(ms + OFF * 1000)
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
for who, _, _, ta, _ in MSGS:
    ms = int(ta * 1000)
    if who == "son": add("sine=f=880:d=0.09,afade=t=out:d=0.09,volume=0.45", ms); add("sine=f=1320:d=0.07,afade=t=out:d=0.07,volume=0.3", ms + 60)
    else: add("anoisesrc=d=0.25:c=white:a=0.4,highpass=f=1500,afade=t=in:d=0.1,afade=t=out:st=0.1:d=0.15,volume=0.5", ms)
k = REPLY_TYPE[0]
while k < REPLY_TYPE[1]:
    add("anoisesrc=d=0.03:c=white:a=0.3,highpass=f=2500,afade=t=out:d=0.03,volume=0.35", int(k * 1000)); k += 0.16
add("sine=f=660:d=0.2,afade=t=out:d=0.2,volume=0.4", 8900)
for f, d in ((523, 0), (659, 80), (784, 160)): add(f"sine=f={f}:d=1.4,afade=t=out:d=1.4,volume=0.3", 18000 + d)
if TRIAL:
    parts.append("anoisesrc=d=0.4:c=pink:a=0.5,highpass=f=800,lowpass=f=5000,afade=t=out:d=0.4,volume=0.6,adelay=250|250[sk]"); labels.append("[sk]")
    parts.append("sine=f=196:d=0.3,afade=t=out:d=0.3,volume=1.2,adelay=900|900[th]"); labels.append("[th]")
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR}"
A = OUT / "sfx.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
MP4 = OUT / "reel.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(MP4)], check=True)
print(MP4)
