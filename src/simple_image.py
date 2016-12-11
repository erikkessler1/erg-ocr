class SimpleImage:

    def __init__(self, im):
        pixels = ["#" if v == 0 else " " for v in list(im.getdata())]
        width, height = im.size

        # make each row a list
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
        self.pixels = pixels


    def __str__(self):
        return "\n".join("".join(d for d in l) for l in self.pixels)
