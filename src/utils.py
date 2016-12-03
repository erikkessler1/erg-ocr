from PIL import Image
"""Collection of utiliy functions"""

def show_in_console(im):
    """Print a black and white picture to the console

    Prints black as '#' and white as ' '.
    Images should be scaled beforehand to fit in the console.

    Args:
        im (Image): Image to print
    """
    # convert black to '#' and white to ' '
    pixels = ["#" if v == 0 else " " for v in list(im.getdata())]
    width, height = im.size

    # make each row a list
    pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

    print("\n".join("".join(d for d in l) for l in pixels))
