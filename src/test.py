from extract import Extractor
from PIL import Image
from utils import is_whitespace, show_in_console

im = Image.open("../images/IMG_0069.jpg")
e = Extractor(im)
for i in e:
    if (i == '\n'):
        print '#'*80
        print '#'*80
    elif (i == '\t'):
        print '#'*80
    else:
        show_in_console(i)
