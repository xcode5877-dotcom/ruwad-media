import sys, subprocess, os
from playwright.sync_api import sync_playwright

FPS = 30
HTML = 'file:///home/claude/reel/reel.html'
SCENES = [(0, 3.0), (3.0, 6.0), (6.0, 10.0), (10.0, 13.0), (13.0, 17.5)]

def page_ctx(pw):
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.goto(HTML)
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    return b, pg

mode = sys.argv[1]
with sync_playwright() as pw:
    b, pg = page_ctx(pw)
    if mode == 'stills':
        os.makedirs('look', exist_ok=True)
        for t in [float(x) for x in sys.argv[2:]]:
            pg.evaluate(f'render({t},{int(t*FPS)})')
            pg.screenshot(path=f'look/t{t:05.2f}.jpg', type='jpeg', quality=85)
    else:
        os.makedirs('scenes', exist_ok=True)
        for i, (a, z) in enumerate(SCENES):
            out = f'scenes/s{i}.mp4'; tmp = f'scenes/s{i}.tmp.mp4'
            ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            f0, f1 = round(a * FPS), round(z * FPS)
            for fi in range(f0, f1):
                pg.evaluate(f'render({fi / FPS},{fi})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait() == 0:
                os.replace(tmp, out)
            print('scene', i, 'done', f1 - f0, 'frames', flush=True)
    b.close()
