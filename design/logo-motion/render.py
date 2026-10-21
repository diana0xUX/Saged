from pathlib import Path
from PIL import Image,ImageFilter,ImageOps,ImageDraw
import numpy as np, subprocess, math
P=Path(__file__).parent; D=P.parent
W=800; FPS=30; DUR=12
names=['SPIRIT','MUSIC','ART']; masks=[]; colors=[]
for name in names:
 p=next(p for p in D.glob('SAGED CLUB*') if name in p.name)
 im=Image.open(p).convert('RGBA'); a=np.array(im); colors.append(a[a[:,:,3]>200,:3].mean(0))
 im.thumbnail((640,456),Image.Resampling.LANCZOS)
 mask=Image.new('L',(W,W)); mask.paste(im.getchannel('A'),((W-im.width)//2,(W-im.height)//2)); masks.append(mask)
Y,X=np.mgrid[:W,:W].astype(float); x=X-W/2;y=Y-W/2
bg=np.array([15,14,19]);
def ease(t): return t*t*(3-2*t)
def warp(mask,amount,phase):
 # Smooth rotational displacement, pinned at the edges.
 r=np.sqrt(x*x+y*y); theta=amount*np.exp(-(r/340)**2)
 sx=np.cos(theta)*x-np.sin(theta)*y+W/2+amount*18*np.sin(y/65+phase)
 sy=np.sin(theta)*x+np.cos(theta)*y+W/2
 arr=np.array(mask,dtype=float); sx=np.clip(sx,0,W-1.001);sy=np.clip(sy,0,W-1.001)
 ix=sx.astype(int);iy=sy.astype(int);fx=sx-ix;fy=sy-iy
 return (arr[iy,ix]*(1-fx)*(1-fy)+arr[iy,ix+1]*fx*(1-fy)+arr[iy+1,ix]*(1-fx)*fy+arr[iy+1,ix+1]*fx*fy)
def frame(t):
 seg=int(t//4)%3; local=t%4; a=masks[seg];b=masks[(seg+1)%3]; c=colors[seg]
 if local<1.7: alpha=np.array(a,dtype=float)
 elif local>=3.4: alpha=np.array(b,dtype=float);c=colors[(seg+1)%3]
 else:
  u=(local-1.7)/1.7;v=ease(u); c=colors[seg]*(1-v)+colors[(seg+1)%3]*v
  if seg==0:
   # Perspective-like card turn, with a tiny elastic overshoot on arrival.
   front=u<.5; q=ease(u*2) if front else ease((u-.5)*2)
   scale=max(.012,math.cos(q*math.pi/2) if front else math.sin(q*math.pi/2))
   src=a if front else b; slim=src.resize((max(1,int(W*scale)),W),Image.Resampling.BICUBIC)
   layer=Image.new('L',(W,W));layer.paste(slim,((W-slim.width)//2,0));alpha=np.array(layer,dtype=float)
   c=colors[seg] if front else colors[(seg+1)%3];c=c*(.65+.35*scale)
  elif seg==1:
   strength=math.sin(math.pi*u); blur=22*strength
   aa=np.array(a.filter(ImageFilter.GaussianBlur(blur)),float);bb=np.array(b.filter(ImageFilter.GaussianBlur(blur)),float)
   field=aa*(1-v)+bb*v; threshold=105-35*strength
   alpha=np.clip((field-threshold)*7+128,0,255)
   if u<.12: alpha=alpha*ease(u/.12)+np.array(a)*(1-ease(u/.12))
   if u>.88: alpha=alpha*(1-ease((u-.88)/.12))+np.array(b)*ease((u-.88)/.12)
  else:
   power=1.9*math.sin(math.pi*u)
   aa=warp(a,power,u*math.pi);bb=warp(b,-power,u*math.pi)
   alpha=aa*(1-v)+bb*v
 alpha=alpha[:,:,None]/255
 return Image.fromarray(np.uint8(np.clip(bg*(1-alpha)+c*alpha,0,255)))
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{W}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'saged-logo-loop.mp4')],stdin=subprocess.PIPE)
for i in range(FPS*DUR):
 im=frame(i/FPS);proc.stdin.write(im.tobytes())
proc.stdin.close(); assert proc.wait()==0
sheet=Image.new('RGB',(W*3,W*2))
for i,t in enumerate([0,2.15,4,6.5,8,10.5]):sheet.paste(frame(t),((i%3)*W,(i//3)*W))
sheet.resize((1200,800)).save(P/'contact-sheet.jpg')
frame(0).save(P/'poster.png')
print('Rendered 12 seconds at 800 × 800 / 30 fps')
