class SimpleImage:
    """Binary representation for an image.

    Stores images as a list rows where each row is a list of '#'/' '.
    This makes it easy to print images to the terminal and easy to
    compare images.

    Attributes:
        pixels (list<list>): The pixels of the image
    """

    def __init__(self, im):
        """SimpleImage constructor

        Args:
            im (Image): The image to convert to a binary representation
        """
        pixels = ["#" if v == 0 else " " for v in list(im.getdata())]
        width, height = im.size

        # make each row a list
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
        self.pixels = pixels


    def __str__(self):
        return "\n".join("".join(d for d in l) for l in self.pixels)
