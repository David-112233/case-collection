"""case-222 manual_v1 程序条件 GT 自查（本地 Chromium，0 API）。用法：python gt_selfcheck.py <html>
只验证程序条件可执行、GT 能通过；GT 选择器（.mobile-screen/.grid-child/.more-info）只用于本 GT 锚定，不进入规则。"""
import sys, json, re, math
from pathlib import Path
from playwright.sync_api import sync_playwright

f = Path(sys.argv[1]).resolve()
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
res, bad = {}, []


def chk(key, ok, val=None):
    res[key] = [bool(ok), val]
    if not ok:
        bad.append(key)


SCREEN_TEXT = {
    1: ['Sign up', "'tis the damn season to get weddings right", 'Email', 'Password', 'Already have an account?', 'Log in here'],
    2: ['Budget', 'Total: $12,000', 'Allocated (Unpaid): $7,000', 'Allocated (Paid): $3,500', 'Remaining: $1,500', 'Allocated Items',
        'Attire', '$ 800', 'DJ', '$ 1200', 'Hair/Makeup', '$ 300', 'Flowers', '$ 750', 'Food', '$ 3,000', 'Venue', '$ 4,500'],
    3: ['Wedding Vision', 'Color Palette', 'Inspiration Gallery'],
    4: ['evermore', 'Your love should be celebrated', 'Sign up for free', 'Already have an account?', 'Log in here'],
    5: ['Checklist', 'Due by March 2021', 'Draft budget', 'Finalize guest list', 'Due by May 2021', 'Research venues', 'Contact venues/Schedule tours',
        'Research caterers', 'Research bakery', 'Due by June 2021', 'Finalize venue + down payment', 'Finalize wedding theme',
        'Research photographers', 'Contact caterers', 'Due by July 2021', 'Food tasting', 'Order save-the-dates'],
    6: ['Vision Board', 'Import and save photos to help you envision your big day', 'Get started'],
    7: ['Guestlist', 'Total Guests: 32', 'Sent?', 'RSVP?', 'Amelia Frost (1)', 'Benji MacKenzie (1)', 'Betty Tang & Family (4)', 'Brandon Steward (1)',
        'Dean Portland (3)', 'Este Rochelle (1)', 'Ivy Rochelle (1)', 'Francine Estella (2)', 'Geller Family (5)', 'Jordan Green (3)'],
    8: ['Wedding Vision', 'Connect your Pinterest account to import images from your selected Pinterest board',
        'Your Pinterest board must be public. We will never post anything to your Pinterest account.', 'Connect now'],
}
SCREEN_URL = {1: ['evermore-background.jpg'], 3: ['evermore-wedding_1.jpg?format=auto'], 4: ['evermore-splash.jpg'],
              6: ['evermore-background.jpg', 'evermore-flowers.jpg?format=auto'], 8: ['evermore-cake.jpg', 'evermore-flowers-2.jpg']}
NAV = ['Checklist', 'Budget', 'Guests', 'Vision']
ACTIVE = {2: 'Budget', 3: 'Vision', 5: 'Checklist', 7: 'Guests', 8: 'Vision'}

JS_SCREENS = r"""()=>{const R=e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]};
return [...document.querySelectorAll('.mobile-screen')].map(s=>{
  const urls=[...s.querySelectorAll('*')].flatMap(e=>{const o=[];if(e.tagName==='IMG')o.push(e.src);const bg=getComputedStyle(e).backgroundImage;(bg.match(/url\("?([^")]+)"?\)/g)||[]).forEach(u=>o.push(u));return o});
  const txt=s.innerText+' '+s.textContent;
  const ph=[...s.querySelectorAll('input')].map(i=>i.placeholder);
  const st=getComputedStyle(s);
  return {box:R(s),w:s.offsetWidth,h:s.offsetHeight,txt,urls,ph,radius:st.borderRadius,shadow:st.boxShadow,overflow:[s,...s.children].map(e=>getComputedStyle(e).overflow).find(v=>v==='hidden'||v==='clip')||st.overflow,
    matrix:getComputedStyle(s.parentElement).transform}})}"""


def lines_y(pg, idx, items):
    """返回每段文字在第 idx 块屏幕中的首次出现 y。"""
    return pg.evaluate("""([i,items])=>{const s=document.querySelectorAll('.mobile-screen')[i];const w=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);const out={};
      while(w.nextNode()){const t=w.currentNode;const v=t.textContent.replace(/\\s+/g,' ').trim();if(!v)continue;
        for(const it of items){if(!(it in out)&&v.includes(it)){const r=document.createRange();r.selectNodeContents(t);const b=r.getBoundingClientRect();out[it]=[b.left,b.top,b.right,b.bottom]}}}
      return out}""", [idx, items])


with sync_playwright() as p:
    br = p.chromium.launch()
    # ---------------- narrow 375x812
    pg = br.new_page(viewport={'width': 375, 'height': 812})
    pg.goto(f.as_uri(), wait_until='networkidle'); pg.wait_for_timeout(800)
    S = pg.evaluate(JS_SCREENS)
    chk('SR-02.C1 count 8', len(S) == 8, len(S))
    chk('SR-02.C2 same size & portrait', len({(s['w'], s['h']) for s in S}) == 1 and S[0]['h'] > S[0]['w'], (S[0]['w'], S[0]['h']))
    chk('SR-02.C3 radius', all(s['radius'] not in ('0px', '') for s in S), S[0]['radius'])
    chk('SR-02.C5 overflow hidden', all(s['overflow'] in ('hidden', 'clip') for s in S), S[0]['overflow'])
    for i, items in SCREEN_TEXT.items():
        t = norm(S[i - 1]['txt'])
        miss = [x for x in items if x not in t]
        chk(f'texts screen {i}', not miss, miss)
    for i, us in SCREEN_URL.items():
        miss = [u for u in us if not any(u in x for x in S[i - 1]['urls'])]
        chk(f'urls screen {i}', not miss, miss)
    chk('SR-06.C5/C6 placeholders', S[0]['ph'] == ['dorothea@gmail.com', 'At least 8 characters'], S[0]['ph'])
    # nav
    nav = pg.evaluate("""()=>[...document.querySelectorAll('.mobile-screen')].map(s=>[...s.querySelectorAll('nav a, nav li, .nav-item, .bottom-nav a, .bottom-nav li, .bottom-nav > *')].map(e=>[e.innerText.trim(),getComputedStyle(e).color]))""")
    res['nav raw (for binding)'] = {i: nav[i - 1] for i in ACTIVE}
    # fonts
    fonts = pg.evaluate("()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family.replace(/\"/g,'')+' '+f.weight)")
    chk('SR-01.C2 / SR-09.C4 fonts loaded', any('Manrope' in x for x in fonts) and any('Big Shoulders Inline Display' in x for x in fonts), fonts)
    # order within screens
    ORD = {1: ['Sign up', "'tis the damn season", 'Email', 'Password', 'Already have an account?', 'Log in here'],
           4: ['evermore', 'Your love should be celebrated', 'Sign up for free', 'Already have an account?'],
           5: ['Due by March 2021', 'Due by May 2021', 'Due by June 2021', 'Due by July 2021'],
           6: ['Vision Board', 'Import and save photos', 'Get started'],
           8: ['Connect your Pinterest', 'Your Pinterest board must be public', 'Connect now']}
    for i, items in ORD.items():
        y = lines_y(pg, i - 1, items)
        ys = [y.get(x, [0, None])[1] for x in items]
        chk(f'order screen {i}', None not in ys and ys == sorted(ys), ys)
    # budget rows: name left, amount right
    b = lines_y(pg, 1, ['Attire', '$ 800', 'Venue', '$ 4,500', 'Total: $12,000', 'Allocated Items'])
    chk('SR-07.C11 name left amount right', b['Attire'][0] < b['$ 800'][0] and abs(b['Attire'][1] - b['$ 800'][1]) < 12, [b['Attire'], b['$ 800']])
    chk('SR-07.C15 card above list', b['Total: $12,000'][1] < b['Allocated Items'][1])
    tw = pg.evaluate("""()=>{const s=document.querySelectorAll('.mobile-screen')[1];const w=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);const o={};while(w.nextNode()){const t=w.currentNode.textContent.trim();if(t.startsWith('Total')||t.startsWith('Remaining'))o[t]=getComputedStyle(w.currentNode.parentElement).fontWeight}return o}""")
    chk('SR-07.C3 Total bold vs lines', int(tw.get('Total: $12,000', 0)) > int(tw.get('Remaining: $1,500', 999)), tw)
    # splash title
    sp = lines_y(pg, 3, ['evermore', 'Your love should be celebrated'])
    sb = S[3]['box']; tmid = (sp['evermore'][1] + sp['evermore'][3]) / 2
    chk('SR-09.C2 upper middle', sb[1] + 0.1 * (sb[3] - sb[1]) < tmid < (sb[1] + sb[3]) / 2, [round(tmid - sb[1]), round(sb[3] - sb[1])])
    chk('SR-09.C3 biggest', (sp['evermore'][3] - sp['evermore'][1]) > 2 * (sp['Your love should be celebrated'][3] - sp['Your love should be celebrated'][1]))
    # sign-up title left aligned with inputs
    al = pg.evaluate("()=>{const s=document.querySelectorAll('.mobile-screen')[0];return [s.querySelector('h2').getBoundingClientRect().left,s.querySelector('input').getBoundingClientRect().left]}")
    chk('SR-06.C4 title left-aligned with input', abs(al[0] - al[1]) < 3, al)
    # hint smaller than description
    fs = pg.evaluate("""()=>{const s=document.querySelectorAll('.mobile-screen')[7];return [...s.querySelectorAll('p,small,span')].filter(e=>e.innerText.trim()).map(e=>[e.innerText.trim().slice(0,20),parseFloat(getComputedStyle(e).fontSize)])}""")
    res['SR-13.C7 font sizes'] = fs
    # narrow layout
    boxes = [s['box'] for s in S]
    chk('SR-17.C1 not tilted', all(s['matrix'] in ('none', 'matrix(1, 0, 0, 1, 0, 0)') or 'matrix(1, 0, 0, 1' in s['matrix'] for s in S), S[0]['matrix'])
    chk('SR-17.C2 single column centered', all(abs(((bx[0] + bx[2]) / 2) - 187.5) < 4 for bx in boxes) and all(boxes[k][3] <= boxes[k + 1][1] for k in range(7)), [round(bx[0]) for bx in boxes])
    chk('SR-17.C4 within viewport width', all(bx[0] >= 0 and bx[2] <= 375 for bx in boxes), [[round(bx[0]), round(bx[2])] for bx in boxes[:1]])
    info = pg.evaluate("()=>{const b=document.querySelector('.more-info').getBoundingClientRect();return [b.left,b.top+scrollY,b.right,b.bottom+scrollY,document.documentElement.scrollHeight]}")
    chk('SR-17.C5 info bar last', info[1] >= boxes[7][3] + pg.evaluate('scrollY') - 1 and abs(info[3] - info[4]) < 2, info)
    chk('SR-17.C6 info bar full width', info[0] == 0 and info[2] == 375, info[:3])
    ib = pg.evaluate("()=>{const m=document.querySelector('.more-info');const a=m.querySelector('a');return [m.innerText.replace(/\\s+/g,' ').trim(),a.innerText.trim(),a.getAttribute('href'),m.querySelector('img').src]}")
    chk('SR-15.C1-C3 info bar', ib[0] == 'Part of the UI Designs inspired by Taylor Swift Album Covers collection. This is evermore (2020).' and ib[2] == 'https://codepen.io/collection/XPxJmz' and ib[3].endswith('palette-evermore.jpg'), ib)
    # D2 hover / focus on both login links and both inputs
    hv = []
    for a in pg.locator('a', has_text='Log in here').all():
        a.scroll_into_view_if_needed(); c0 = a.evaluate('e=>getComputedStyle(e).color'); a.hover(); pg.wait_for_timeout(300)
        c1 = a.evaluate('e=>getComputedStyle(e).color'); pg.mouse.move(2, 2); pg.wait_for_timeout(300); hv.append([c0, c1, a.evaluate('e=>getComputedStyle(e).color')])
    chk('DR-01.C1 hover orange', all(h[1] == 'rgb(245, 147, 0)' and h[0] != h[1] for h in hv), hv)
    chk('DR-01.C2 restore', all(h[2] == h[0] for h in hv))
    fo = []
    for i in pg.locator('.mobile-screen').first.locator('input').all():
        q = 'e=>[getComputedStyle(e).borderBottomWidth,getComputedStyle(e).boxShadow,getComputedStyle(e).outlineStyle]'
        s0 = i.evaluate(q); i.click(); pg.wait_for_timeout(200); s1 = i.evaluate(q); pg.mouse.click(2, 2); pg.wait_for_timeout(200); fo.append([s0, s1, i.evaluate(q)])
    chk('DR-02.C1 thicker on focus', all(x[1][1] != 'none' and x[0][1] == 'none' for x in fo), fo)
    chk('DR-02.C2 no outline', all(x[1][2] == 'none' for x in fo))
    chk('DR-02.C3 restore', all(x[2] == x[0] for x in fo))
    pg.close()

    # ---------------- wide 1440x900
    pg = br.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(f.as_uri(), wait_until='networkidle'); pg.wait_for_timeout(800)
    sbw = pg.evaluate("()=>[innerWidth-document.documentElement.clientWidth,innerHeight-document.documentElement.clientHeight]")
    pg.mouse.move(720, 450); pg.mouse.wheel(0, 3000); pg.keyboard.press('End'); pg.keyboard.press('PageDown'); pg.wait_for_timeout(400)
    chk('SR-16.C1 no scrollbar & no scroll', sbw == [0, 0] and pg.evaluate('[scrollX,scrollY]') == [0, 0], sbw)
    W = pg.evaluate(JS_SCREENS)
    cen = [((s['box'][0] + s['box'][2]) / 2, (s['box'][1] + s['box'][3]) / 2) for s in W]
    cols_ok = all(cen[2 * k][1] < cen[2 * k + 1][1] for k in range(4)) and all(cen[2 * k][0] < cen[2 * k + 2][0] for k in range(3))
    chk('SR-16.C2 four columns ①②/③④/⑤⑥/⑦⑧', cols_ok, [[round(x), round(y)] for x, y in cen])
    m = W[0]['matrix']; a, bb = [float(v) for v in re.findall(r'-?[\d.]+', m)[:2]]
    angs = []
    for s in W:
        mm = [float(v) for v in re.findall(r'-?[\d.e]+', s['matrix'])[:2]]
        angs.append(round(math.degrees(math.atan2(mm[1], mm[0])), 1))
    chk('SR-16.C5/C6 clockwise & uniform tilt', all(x > 5 for x in angs) and len(set(angs)) == 1, angs)
    gc = pg.evaluate("()=>[...document.querySelectorAll('.grid-child')].map(e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]})")
    tops = [W[2 * k]['box'][1] for k in range(4)]
    chk('SR-16.C7 col2 highest, col4 lowest', tops.index(min(tops)) == 1 and tops.index(max(tops)) == 3, [round(t) for t in tops])
    gx = (min(g[0] for g in gc) + max(g[2] for g in gc)) / 2
    res['SR-16.C4 group center dx'] = round(gx - 720)
    ib = pg.evaluate("()=>{const b=document.querySelector('.more-info').getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]}")
    chk('SR-16.C8 info top-right', ib[1] == 0 and ib[2] == 1440, ib)
    res['SR-16.C9 info width ratio'] = round((ib[2] - ib[0]) / 1440, 3)
    top = pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);return !!e.closest('.more-info')}", [ib[0] + 20, ib[3] - 10])
    chk('SR-16.C10 info over screens', top)
    scale = (W[0]['box'][2] - W[0]['box'][0]) / (450 * math.cos(math.radians(20)) + 800 * math.sin(math.radians(20)))
    gaps = [math.dist(cen[2 * k], cen[2 * k + 1]) - 800 * scale for k in range(4)]
    chk('SR-16.C3 gap along tilted column axis', all(g > 5 for g in gaps), [round(g) for g in gaps])
    br.close()

print(json.dumps(res, ensure_ascii=False, indent=1))
print('FAILED:', bad)
