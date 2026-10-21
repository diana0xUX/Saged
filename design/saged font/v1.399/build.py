from pathlib import Path
import shutil, importlib.util
from PIL import Image
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.svgLib.path import parse_path
from xml.etree import ElementTree as ET
HERE=Path(__file__).resolve().parent
OLD=Path('/Users/diana/Downloads/codex-design-studio/projects/saged-display-cyrillic')
# Snapshot editable construction source and all dependencies for reproducibility.
if not (HERE/'sources/glyph-sources').exists(): shutil.copytree(OLD/'src/glyph-sources',HERE/'sources/glyph-sources')
for name in ['euro sign.svg','letter-042b-Ы.svg','Vector.svg','Group 441.png']:
 if not (HERE/'sources'/name).exists(): shutil.copy2(HERE.parent/name,HERE/'sources'/name)
costa=OLD.parents[1]/'brand-system/design-system/public/fonts/costa-light.otf'
if not (HERE/'sources/costa-light.otf').exists(): shutil.copy2(costa,HERE/'sources/costa-light.otf')
if not (HERE/'sources/base_builder.py').exists():
 src=(OLD/'src/build_font.py').read_text().replace('1.398','1.399').replace('1398','1399')
 (HERE/'sources/base_builder.py').write_text(src)
spec=importlib.util.spec_from_file_location('builder',HERE/'sources/base_builder.py'); b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
for key,value in list(vars(b).items()):
 if isinstance(value,Path) and str(value).startswith(str(b.ROOT/'src/glyph-sources')):
  setattr(b,key,HERE/'sources/glyph-sources'/value.relative_to(b.ROOT/'src/glyph-sources'))
b.OUT=HERE;b.COSTA_SOURCE=HERE/'sources/costa-light.otf';b.EURO_SOURCE=HERE/'sources/euro sign.svg'
# Trace the supplied transparent PNG boundary; simplify subpixel stair steps.
im=Image.open(HERE/'sources/Group 441.png').convert('RGBA');w,h=im.size
filled={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))[3]>=128}
edges={}
for x,y in filled:
 for neighbor,a,z in [((x,y-1),(x,y),(x+1,y)),((x+1,y),(x+1,y),(x+1,y+1)),((x,y+1),(x+1,y+1),(x,y+1)),((x-1,y),(x,y+1),(x,y))]:
  if neighbor not in filled: edges[a]=z
loops=[]
while edges:
 start=next(iter(edges));p=start;pts=[]
 while p in edges:
  pts.append(p);p=edges.pop(p)
  if p==start:break
 if len(pts)>20:loops.append(pts)
def rdp(p,e=.65):
 if len(p)<3:return p
 a,z=p[0],p[-1];dx=z[0]-a[0];dy=z[1]-a[1];den=(dx*dx+dy*dy)**.5 or 1
 ds=[abs(dy*(x-a[0])-dx*(y-a[1]))/den for x,y in p]
 i=max(range(len(ds)),key=ds.__getitem__)
 return rdp(p[:i+1],e)[:-1]+rdp(p[i:],e) if ds[i]>e else [a,z]
paths=[]
for pts in loops:
 k=len(pts)//2;p=rdp(pts[:k+1])[:-1]+rdp(pts[k:]+[pts[0]])[:-1]
 mids=[((p[i][0]+p[(i+1)%len(p)][0])/2,(p[i][1]+p[(i+1)%len(p)][1])/2) for i in range(len(p))]
 d=f'M{mids[-1][0]} {mids[-1][1]} '+ ' '.join(f'Q{x} {y} {mids[i][0]} {mids[i][1]}' for i,(x,y) in enumerate(p))+' Z'
 paths.append((min(y for x,y in pts),max(y for x,y in pts),d))
(HERE/'sources/short-i-traced.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 105 148">'+''.join(f'<path d="{d}"/>' for _,__,d in paths)+'</svg>')
def short_i():
 pen=TTGlyphPen(None);body=max(paths,key=lambda p:p[1]-p[0]);scale=735/(body[1]-body[0])
 for top,bottom,d in paths:
  sy=scale if (top,bottom,d)==body else 164/(bottom-top)
  offset=bottom*sy if (top,bottom,d)==body else 919+top*sy
  parse_path(d,TransformPen(Cu2QuPen(pen,max_err=.7,reverse_direction=True),(scale,0,0,-sy,64,offset)))
 return pen.glyph(),round(w*scale+128)
original=b.draw_letter
def draw(ch):
 if ch=='Й':return short_i()
 if ch=='Ы':return b.supplied_svg_glyph(HERE/'sources/letter-042b-Ы.svg')
 if ch=='Ю':return b.supplied_svg_glyph(HERE/'sources/Vector.svg')
 return original(ch)
b.draw_letter=draw
b.main()
