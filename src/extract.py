import sys
from PIL import Image, ImageFilter

class Extractor:
    """Extract charaters from the image of an erg screen

    This class implements the iterator protocol allowing
    the user to iterate through all charaters found in the image.
    It returns the charaters as images.

    This class will give the user the opportunity to adjust the rotation
    of the image in the terminal before searching for charaters.

    Attributes:
        im (Image): the transformed image it is extracting from

    """

    # Below becomes black, above becomes white
    BW_THRESHOLD = 150

    # Size of image when priting in console
    CONSOLE_SIZE = (128,170)

    # Box of the inital crop of the image
    INITAL_CROP = (300,808,2048,2556)

    # Final size of the image after transformation
    FINAL_SIZE = (462,462)

    # number of switches for being in a lines
    SWITCH_THRESHOLD = 20

    # number of black pixels for being in a chars
    BLACK_COUNT_THRESHOLD = 2

    def __init__(self, im):
        """Extractor constructor

        Creating an Extractor will prompt the user in the terminal
        to rotate the image.

        Args:
            im (Image): Image to extract from

        """
        # transform the image
        self.im = transform(im)

        # private attributes for the iteration
        self.__chpos = 0
        self.chars = find_chars(self.im)

    def __transform(im):
        """Rotate, convert to black and white, and resize the image

        Allows the user to specify the image rotation. Then crops
        and resizes it and converts it to black and white.

        Args:
            im (Image): Image to transform

        Returns:
            Image: the transformed image

        """

        # convert to greyscale (L mode) and apply inital rotation
        transformed = im.convert("L").rotate(-90, expand=True)

        # convert to black and white
        bwdata = [0 if v <= BW_THRESHOLD else 255 for v in list(transformed.getdata())]
        transformed.putdata(bwdata)

        # allow the user to rotate the image
        while True:
            show_in_console(transformed.resize(CONSOLE_SIZE, Image.BILINEAR))
            rotate = int(input("Rotate: "))
            if (rotate == 0):
                break
            transformed = transformed.rotate(rotate, expand=True)

        # crop and resize it to its final size
        transformed = transformed.crop(INITAL_CROP).resize(FINAL_SIZE, Image.BILINEAR)

        # recompute the black and white data because rotation/resizing blurs it
        bwdata = [0 if v <= BW_THRESHOLD else 255 for v in list(transformed.getdata())]
        transformed.putdata(bwdata)

        return transformed

    def find_chars(im):
        """Finds suspected charaters in the image

        Splits the image into lines and charaters based on white space.

        Args:
            im (Image): Pre-transformed (croped, b/w) image to extract from

        Returns:
            List of 4-tuples of the left, top, right, bottom coordinates
            of suspected charaters
        """

        def get_lines(pixels):
            """Gets top and bottoms of lines

            Determines lines by looking at the number of switches from 1s to 0s.
            If there are few switches it likely doesn't have charaters.

            Args:
                pixels (2D list): image encoded as 0 and 1

            Return:
                List of 2-tuples (top, bottom)
            """
            lines = []
            top = 0
            inline = False

            # iterate through each row of pixels
            for r in range(0, height):
                switches = 0
                current = pixels[r][0]
                for c in range(0, width):
                    new = pixels[r][c]

                    # check for a switch
                    if (new != current):
                        switches += 1
                        current = new

                # check if in a line or not
                if (inline):
                    # if in a line and below threshold, the line is over
                    if (switches < SWITCH_THRESHOLD):
                        # remove small lines as they are probably garbage
                        if ((r-1) - top > 15):
                            lines.append((top, r-1))
                        inline = False
                else:
                    # if not in line but above threshold, entering a line
                    if (switches >= SWITCH_THRESHOLD):
                        inline = True
                        top = r

            return lines

        def get_chars(pixels, lines):
            """Look though each line for charaters

            Args:
                pixels (2D list): image encoded as 0 and 1
                lines (list: (int, int)): top and bottom of lines
            Return:
                List of 4-tuples of the left, top, right, bottom coordinates
                of suspected charaters
            """
            chars = []

            # look through each line
            for top, bottom in lines:
                left = 0
                inchar = False

                # move from left to right through the line
                for c in range(0, width):
                    count = 0

                    # count black pixels in the column
                    for r in range(top, bottom + 1):
                        if (pixels[r][c] == 1):
                            count += 1

                    # check if in a character or not
                    if (inchar):
                        # if in a charater and below threshold, leave the charater
                        if (count < BLACK_COUNT_THRESHOLD):

                            # if the character is too wide, split it in half as it is likely
                            # a joined character
                            if ((c-1) - left > 25):
                                half = int(((c-1) - left)/2)
                                chars.append((left, top, left + half, bottom))
                                chars.append((left + half + 1, top, c-1, bottom))
                            else:
                                chars.append((left, top, c-1, bottom))
                            inchar = False
                    else:
                        # if not in a character and above threshold, enter the character
                        if (count >= BLACK_COUNT_THRESHOLD):
                            inchar = True
                            left = c

            return chars

        pixels = [1 if v == 0 else 0 for v in list(im.getdata())]
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

        return get_chars(pixels, get_lines(pixels))


    def __iter__(self):
        return self

    def next(self):
        # check that this is not the last line
        if (self.chpos < len(self.chars)):
            # crop around the next character
            c = self.im.crop(self.chars[chpos])
            # increment to the next charater
            chpos += 1
            return c
        else:
            raise StopIteration()
