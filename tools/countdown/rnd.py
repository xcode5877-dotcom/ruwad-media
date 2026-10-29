import sys, subprocess, os, json
from playwright.sync_api import sync_playwright
# usage: rnd.py page.html outdir stills t1 t2 ... | rnd.py page.html outdir scenes 0,2.8,12.1,15,18
FPS=30
html, out, mode = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/reel/'+html); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    if mode == 'stills':
        for t in map(float, sys.argv[4:]):
            pg.evaluate(f'render({t},{int(t*FPS)})'); pg.wait_for_timeout(50)
            pg.screenshot(path=f'{out}/t{t:05.2f}.jpg', type='jpeg', quality=85)
    else:
        cuts = list(map(float, sys.argv[4].split(',')))
        names=[]
        for i,(a,z) in enumerate(zip(cuts, cuts[1:])):
            tmp=f'{out}/s{i}.tmp.mp4'; fin=f'{out}/s{i}.mp4'
            ff = subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),tmp], stdin=subprocess.PIPE)
            for fi in range(round(a*FPS), round(z*FPS)):
                pg.evaluate(f'render({fi/FPS},{fi})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait()==0: os.replace(tmp, fin)
            names.append(f"file 's{i}.mp4'")
        open(f'{out}/list.txt','w').write('\n'.join(names)+'\n')
    b.close()
