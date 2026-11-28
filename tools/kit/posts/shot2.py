import sys,os
from playwright.sync_api import sync_playwright
f,w,h,n=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]); pre=sys.argv[5] if len(sys.argv)>5 else ''
d=os.path.abspath('.')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':h})
    for i in range(1,n+1):
        pg.goto(f'file://{d}/{f}?s={pre}{i}'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'out/{f.split(".")[0]}-{i}.jpg',type='jpeg',quality=93)
    b.close()
