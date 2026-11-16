import sys
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); d = ImageDraw.Draw(im)
w, h = im.size
for x in range(0, w, 50):
    d.line([(x,0),(x,h)], fill=(255,0,0) if x%100==0 else (255,180,180), width=1)
    if x%100==0: d.text((x+2,2), str(x), fill=(255,0,0))
for y in range(0, h, 50):
    d.line([(0,y),(w,y)], fill=(0,0,255) if y%100==0 else (180,180,255), width=1)
    if y%100==0: d.text((2,y+2), str(y), fill=(0,0,255))
im.save(out)
