#!/usr/bin/env python3
"""Generate Fincraft's original, ASCII-only 'Systems Core' illustration.
No external image, photo, or logo is embedded in the SVG.
Requires Pillow + CairoSVG only for the PNG preview; SVG generation uses stdlib.
"""
from pathlib import Path
import math, random, html
P = Path(__file__).resolve().parents[1]
ASSETS = P / 'profile' / 'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
C, R = 112, 68
chars = [[' ']*C for _ in range(R)]
prios = [[-1]*C for _ in range(R)]
colrs = [[0]*C for _ in range(R)]
random.seed(1408)

def put(x,y,ch='.',prio=0,tone=1):
 x,y=int(round(x)),int(round(y))
 if 0<=x<C and 0<=y<R and prio>=prios[y][x]:
  chars[y][x]=ch; prios[y][x]=prio; colrs[y][x]=tone

def shape_line(a,b,prio=2,tone=2,dash=1):
 x0,y0=a; x1,y1=b
 length=math.hypot(x1-x0,y1-y0)
 n=int(length*3)+1
 dx=x1-x0;dy=y1-y0
 stroke=('-' if abs(dx)>abs(dy)*2.35 else '|' if abs(dy)>abs(dx)*1.5 else '\\' if dx*dy>0 else '/')
 for i in range(n+1):
  if dash>1 and (i//4)%dash==dash-1:continue
  x=x0+dx*i/n;y=y0+dy*i/n
  put(x,y,stroke,prio,tone)

def poly(v,prio=2,tone=2):
 for a,b in zip(v,v[1:]+v[:1]):shape_line(a,b,prio,tone)
 for x,y in v:put(x,y,'+',prio+1,3)

def label(x,y,s,prio=10,tone=4):
 for k,ch in enumerate(s):put(x+k,y,ch,prio,tone)

# Quiet scaffold dots / sensor field around central shape.
for _ in range(780):
 x=random.randrange(3,C-1);y=random.randrange(2,R-2)
 d=((x-55)/51)**2+((y-34)/35)**2
 if 0.50<d<1.28 and random.random()<.62:
  put(x,y,random.choices(['.',':','+'],[15,3,1])[0],0,0)

# Isometric computation lattice: paired hexagons form a dimensional frame.
cx,cy=54,34
outer=[(cx,cy-29),(cx+35,cy-15),(cx+35,cy+15),(cx,cy+29),(cx-35,cy+15),(cx-35,cy-15)]
back=[(x+7,y-6) for x,y in outer]
poly(back,1,1)
for a,b in zip(outer,back):shape_line(a,b,1,1)
poly(outer,3,2)
# Nested geometric shell, distinct from brand logo.
inner=[(cx,cy-22),(cx+25,cy-11),(cx+25,cy+11),(cx,cy+22),(cx-25,cy+11),(cx-25,cy-11)]
poly(inner,2,2)
for i,(a,b) in enumerate(zip(outer,inner)):
 shape_line(a,b,2,1,dash=3)
# Triangular data grid, with selectively illuminated routes.
for i in range(6):
 if i%2==0:
  shape_line(inner[i],inner[(i+2)%6],1,1,dash=3)
# Latitudinal and longitude computational orbits rendered with ASCII glyphs.
def orbit(rx,ry,rot,start=0,end=2*math.pi,prio=2,tone=2,broken=False):
 cs,sn=math.cos(rot), math.sin(rot)
 for k in range(1650):
  t=start+(end-start)*k/1649
  x=rx*math.cos(t); y=ry*math.sin(t)
  px=cx+x*cs-y*sn; py=cy+x*sn+y*cs
  if broken and (int(t*22)%8) in (5,6,7):continue
  # Use partial line hints instead of fully thick orbit walls
  put(px,py,'.' if k%9<3 else ':' if k%9<7 else '*',prio,tone)
orbit(44,12,-.38,prio=2,tone=1,broken=True)
orbit(26,29,.51,prio=1,tone=1,broken=True)
orbit(36,22,-.88,prio=1,tone=1,broken=True)

# Encoded active connections and well-spaced endpoint lights.
traces=[((19,34),(32,34)),((81,19),(102,10)),((83,52),(105,61)),((40,8),(25,3)),((33,61),(19,65)),((90,33),(103,33))]
for j,(a,b) in enumerate(traces):
 shape_line(a,b,3,2,dash=2)
 put(*b,'o',4,3)
 if j%2==0:put(b[0]-2,b[1],'*',4,4)
for x,y in [(14,14),(98,15),(107,44),(11,56),(65,1),(29,33),(89,37),(54,4),(56,63)]:
 put(x,y,'+',3,2);put(x+2,y,'.',0,1)

# The engine module floating at the centre. Thin ASCII outlines create an
# identifiable technology artifact without reproducing a corporate logo.
chip=(43,25,67,43)
x0,y0,x1,y1=chip
for x in range(x0,x1+1):
 put(x,y0,'-',7,3);put(x,y1,'-',7,3)
for y in range(y0,y1+1):
 put(x0,y,'|',7,3);put(x1,y,'|',7,3)
for x in (x0,x1):
 for y in (y0,y1):put(x,y,'+',8,4)
for xx in range(x0+2,x1-1,4):
 put(xx,y0-2,'|',5,2);put(xx,y1+2,'|',5,2)
 put(xx,y0-1,'+',6,3);put(xx,y1+1,'+',6,3)
for yy in range(y0+3,y1-1,4):
 for x,ch in [(x0-2,'-'),(x0-1,'+'),(x1+1,'+'),(x1+2,'-')]:put(x,yy,ch,5,2)
for y in range(y0+2,y1-1):
 for x in range(x0+2,x1-1):
  if (x*17+y*11)%41==0:put(x,y,'.',4,0)
label(x0+4,y0+4,'SYS / CORE',10,4)
label(x0+4,y0+7,'------------',10,2)
label(x0+4,y0+10,'0101  /  AI',10,3)
label(x0+4,y0+13,'> BUILD_   ',10,4)
# Light packets on the outer boundary.
for x,y in [outer[0],outer[2],outer[4],inner[1],inner[3],inner[5]]:
 put(x,y,'@',6,4)

art='\n'.join(''.join(row).rstrip() for row in chars)+'\n'
(ASSETS/'systems-core-ascii.txt').write_text(art,encoding='utf-8')

BG='#0d1117';BORDER='#30363d';WHITE='#edf2f7';BODY='#b9c3ce';MUTED='#87949f';ACC='#8ee1cd';ACCLOW='#72b8ae'
PALETTE=['#43535f','#697b87','#99adb9','#cfdae3',ACC]
W,H=1360,960
cw,ch=6.55,10.65
artx,arty=33,123
svg=[]
def add(s):svg.append(s)
def t(x,y,txt,size=18,color=BODY,weight=400,anchor=None,letter_spacing=None):
 attrs=f'x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}"'
 if anchor: attrs+=f' text-anchor="{anchor}"'
 if letter_spacing: attrs+=f' letter-spacing="{letter_spacing}"'
 add(f'<text {attrs}>{html.escape(txt)}</text>')
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ttl dsc">')
add('<title id="ttl">Fincraft — Systems Core ASCII and engineering profile</title>')
add('<desc id="dsc">An original ASCII illustration of a computational core, followed by company focus, Wavern product, and technical work.</desc>')
add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
add(f'<rect x="10" y="10" width="1340" height="940" fill="none" stroke="{BORDER}" stroke-width="1.5"/>')
add('<g font-family="DejaVu Sans Mono, Liberation Mono, monospace">')
t(34,43,'fincraft / README.md',17,WHITE)
t(1323,43,'ENGINEERING / ASCII EDITION',15,MUTED,anchor='end')
add(f'<path d="M34 59 H1325 M810 76 V873 M34 903 H1325" stroke="{BORDER}" stroke-width="1.5" fill="none"/>')
t(34,88,'01 / SYSTEMS CORE',14,MUTED)
t(845,98,'02 / PROFILE',16,MUTED)
# Print each contiguous tonal run at a precisely positioned x-coordinate.
add(f'<g font-size="11" xml:space="preserve">')
for y,row in enumerate(chars):
 if y>67:break
 xpos=0
 while xpos<C:
  if row[xpos]==' ':xpos+=1;continue
  color_id=colrs[y][xpos]
  j=xpos+1
  while j<C and row[j]!=' ' and colrs[y][j]==color_id:j+=1
  segment=''.join(row[xpos:j]);tx=artx+xpos*cw;ty=arty+y*ch
  add(f'<text x="{tx:.2f}" y="{ty:.2f}" fill="{PALETTE[color_id]}">{html.escape(segment)}</text>')
  xpos=j
add('</g>')
# right copy, concise and easily updateable
x=844
t(x,173,'FINCRAFT',49,WHITE,700,letter_spacing='-0.6')
t(x,205,'SOFTWARE  /  INTELLIGENCE  /  SYSTEMS',15,ACC)
add(f'<path d="M{x} 231 H1316" stroke="{BORDER}" stroke-width="1.5"/>')
t(x,275,'$ whoami',19,WHITE)
t(x,309,'A software company building',17,BODY)
t(x,336,'products, AI, and useful systems.',17,BODY)
t(x,390,'$ tree ./focus',19,WHITE)
t(x,429,'|-- products      SaaS & digital tools',16,BODY)
t(x,461,'|-- engineering   APIs & platforms',16,BODY)
t(x,493,'|-- intelligence  AI & automation',16,BODY)
t(x,525,'`-- lab           prototypes & ideas',16,BODY)
t(x,583,'$ featured_product',19,WHITE)
t(x,618,'Wavern',19,ACC,600)
t(x+85,618,'/ Accounting platform',16,BODY)
t(x,667,'$ current_state',19,WHITE)
t(x,701,'building  ->  testing  ->  evolving',16,BODY)
t(x,754,'$ connect',19,WHITE)
t(x,790,'wavern.com.br',17,ACC)
t(x,827,'Projects ship here as they grow.',15,MUTED)
t(34,933,'IDEA  >  CODE  >  SYSTEM  >  PRODUCT',16,BODY)
t(1325,933,'FINCRAFT / BUILD WHAT MATTERS',15,MUTED,anchor='end')
add('</g></svg>')
(ASSETS/'fincraft-ascii.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
try:
 import cairosvg
 cairosvg.svg2png(url=str(ASSETS/'fincraft-ascii.svg'),write_to=str(ASSETS/'fincraft-preview.png'), output_width=1360, output_height=960)
 print('Generated PNG, SVG, ASCII',len(art),'characters; SVG',len('\n'.join(svg)),'bytes')
except ImportError:print('SVG and TXT generated. pip install cairosvg to generate PNG preview.')
