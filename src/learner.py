from PIL import Image
from extract import Extractor
import os.path

with open("../training_data.txt", "a+") as f:
    FILE_PATH = "../images/IMG_0069.jpg"
    IM_NAME = os.path.basename(FILE_PATH)
    im = Image.open(FILE_PATH)
    e = Extractor(im)
    for s_im in e:
        if (not Extractor.is_whitespace(s_im)):
            print s_im

            digit = input("Input value: ")
            f.write("Digit: {} \n".format(digit))
            f.write("File: {}\n".format(IM_NAME))

            f.write(str(s_im))
            f.write("\n@\n")


"""
Digit: l
File: lol
[PIXEL DATA]
@
"""
