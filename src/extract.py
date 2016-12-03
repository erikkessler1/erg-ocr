import sys
from PIL import Image, ImageFilter

im = Image.open(sys.argv[1]).convert("L").rotate(-89, expand=True)
im = im.crop((300,808,2048,2556)).resize((462,462), Image.BILINEAR)

bwdata = [0 if v <= 150 else 255 for v in list(im.getdata())]
im.putdata(bwdata)

pixels = [1 if v == 0 else 0 for v in list(im.getdata())]
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

lines = []
top = 0
inline = False
for r in range(0, height):
    switches = 0
    current = pixels[r][0]
    for c in range(0, width):
        new = pixels[r][c]
        if (new != current):
            switches += 1
            current = new
    if (inline):
        if (switches < 20):
            if ((r-1) - top > 15):
                lines.append((top, r-1))
            inline = False
    else:
        if (switches >= 20):
            inline = True
            top = r

print (lines)

im.show()
for top,bottom in lines:
    #im.crop((0,top,width,bottom)).show()

    chars = []
    start = 0
    inchar = False
    for c in range(0, width):
        count = 0
        for r in range(top, bottom + 1):
            if (pixels[r][c] == 1):
                count += 1
        if (inchar):
            if (count < 2):
                if ((c-1) - start > 25):
                    half = int(((c-1) - start)/2)
                    chars.append((start, start + half))
                    chars.append((start + half + 1, c-1))
                else:
                    chars.append((start,c-1))
                inchar = False
        else:
            if (count >= 2):
                inchar = True
                start = c

    print(chars)
    for start, end in chars:
        im.crop((start,top,end,bottom)).show()
    break
#print("".join("".join(str(d) for d in l) for l in pixels))
