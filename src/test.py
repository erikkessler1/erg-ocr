from extract import Extractor
from PIL import Image

im = Image.open("../images/IMG_0069.jpg")
e = Extractor(im)
for i in e:
    if (i == '\n'):
        print '#'*80
        print '#'*80
    elif (i == '\t'):
        print '#'*80
    else:
        print i
