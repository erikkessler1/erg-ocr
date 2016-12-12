class SimpleImage:
    """Binary representation for an image.

    Stores images as a list rows where each row is a list of '#'/' '.
    This makes it easy to print images to the terminal and easy to
    compare images.

    Attributes:
        pixels (list<list>): The pixels of the image
    """

    def __init__(self, pixels):
        """SimpleImage constructor

        Args:
            pixels (list<list>): The pixels of the image
        """
        self.pixels = pixels

    @classmethod
    def fromImage(cls, im):
        pixels = ["#" if v == 0 else " " for v in list(im.getdata())]
        width, height = im.size

        # make each row a list
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
        return cls(pixels)

    @classmethod
    def fromString(cls, str):
        return cls([list(l) for l in str.split('\n')])

    def __str__(self):
        return "\n".join("".join(d for d in l) for l in self.pixels)
