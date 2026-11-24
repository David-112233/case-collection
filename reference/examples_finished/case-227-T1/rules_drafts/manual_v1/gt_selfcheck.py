import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
p = Path(sys.argv[1])
JS = """() => {
 const imgs=[...document.images].map(i=>{const r=i.getBoundingClientRect();return {src:i.currentSrc,alt:i.alt,x:r.x,y:r.y,w:r.width,h:r.height,r:r.right,b:r.bottom,nw:i.naturalWidth,nh:i.naturalHeight,ow:i.offsetWidth,oh:i.offsetHeight,t:getComputedStyle(i).transform,bs:getComputedStyle(i).boxShadow}});
 imgs.sort((a,b)=>a.y-b.y);
 return {vw:innerWidth, imgs};
}"""
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 900})
    pg.goto(p.as_uri(), wait_until='networkidle')
    pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
    d = pg.evaluate(JS); br.close()
vw = d['vw']; im = d['imgs']; fl = sorted(im[:4], key=lambda a: a['x']); le = sorted(im[4:], key=lambda a: a['x'])
names = ['tahani', 'jason', 'chidi', 'eleanor']
res = {}
res['SR-02.C1/SR-03.C1 count'] = (len(fl), len(le))
res['SR-02 order'] = all(names[i] in fl[i]['src'] for i in range(4))
res['SR-03 order'] = all(names[i] in le[i]['src'] for i in range(4))
res['alt'] = all(a['alt'].lower().startswith(n) and a['alt'].endswith('from The Good Place') for g in (fl, le) for a, n in zip(g, names))
res['float center L/R'] = (round(fl[0]['x'], 1), round(vw - fl[-1]['r'], 1))
res['float row tops'] = [round(a['y'], 1) for a in fl]
res['float widths'] = [round(a['w'], 1) for a in fl]
res['float gaps'] = [round(fl[i+1]['x'] - fl[i]['r'], 1) for i in range(3)]
res['float ratio diff'] = [round(a['w']/a['h'] - a['nw']/a['nh'], 4) for a in fl]
res['float transform/boxshadow'] = [(a['t'], a['bs']) for a in fl]
res['lean center offset'] = round((le[0]['x'] + le[-1]['r'])/2 - vw/2, 1)
res['lean pair gaps (bbox)'] = [round(le[i+1]['x'] - le[i]['r'], 1) for i in range(3)]
res['lean bottoms'] = [round(a['b'], 1) for a in le]
res['lean heights'] = [round(a['h'], 1) for a in le]
res['size lean/float avg w,h'] = (round(sum(a['w'] for a in le)/sum(a['w'] for a in fl), 3), round(sum(a['h'] for a in le)/sum(a['h'] for a in fl), 3))
res['groups vertical gap'] = round(min(a['y'] for a in le) - max(a['b'] for a in fl), 1)
print(json.dumps(res, ensure_ascii=False, indent=1))
