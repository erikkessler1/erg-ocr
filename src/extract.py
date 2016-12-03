import sys
from PIL import Image, ImageFilter

class Extractor:
    """Extract charaters from the image of an erg screen

    This class implements the iterator protocol allowing
    the user to iterate through all charaters found in the image.
    It returns the charaters as images.

    This class will give the user the opportunity to adjust the rotation
    of the image in the terminal before searching for charaters.

    """

    def __init__(self, im):
        """Extractor constructor

        Creating an Extractor will prompt the user in the terminal
        to rotate the image.

        Args:
            im (Image): Image to extract from

        """
        # private attributes for the iteration
        self.__lines = []
        self.__chars = []
        self.__lnpos = 0
        self.__chpos = 0

        # the image
        self.__im = im

    def __iter__(self):
        return self

    def next(self):
        # check that this is not the last line
        if (self.lnpos < len(lines)):
            # crop out the next charact
            top, bottom = lines[lnpos]
            left, right = chars[chpos]
            c = self.im.crop((left, top, right, bottom))

            # increment to the next charater
            chpos += 1
            if (chpos == len(chars)):
                chpos = 0
                lnpos += 1 # go to the next line if needed

            return c
        else:
            raise StopIteration()


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
