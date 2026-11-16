import fitz, sys
d = fitz.open(sys.argv[1])
print(len(d), "pages", d[0].rect)
for i, pg in enumerate(d):
    pg.get_pixmap(dpi=int(sys.argv[2]) if len(sys.argv)>2 else 70).save(f"prev_{i+1}.png")
