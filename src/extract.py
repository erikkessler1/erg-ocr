import sys
from PIL import Image, ImageFilter

class Extractor:
    def __init__(self, im):
        self.lines = []
        self.chars = []
        self.lnpos = 0
        self.chpos = 0

        self.im = im

    def __iter__(self):
        return self

    def next(self):
        if (self.lnpos < len(lines)):
            top, bottom = lines[lnpos]
            left, right = chars[chpos]
            c = self.im.crop((left, top, right, bottom))

            chpos += 1
            if (chpos == len(chars)):
                chpos = 0
                lnpos += 1
        else:
            raise StopIteration()

def show_in_console(im):
    pixels = ["#" if v == 0 else " " for v in list(im.getdata())]
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    print("\n".join("".join(d for d in l) for l in pixels))

im = Image.open(sys.argv[1]).convert("L").rotate(-90, expand=True)
bwdata = [0 if v <= 150 else 255 for v in list(im.getdata())]
im.putdata(bwdata)

show_in_console(im.resize((128,170), Image.BILINEAR))
rotate = int(input("Rotate: "))
while (rotate != 0):
    im = im.rotate(rotate, expand=True)
    show_in_console(im.resize((128,170), Image.BILINEAR))
    rotate = int(input("Rotate: "))

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
        show_in_console(im.crop((start,top,end,bottom)))
        print("\n")
    break
