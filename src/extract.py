import sys
from PIL import Image, ImageFilter
from simple_image import SimpleImage

class Extractor:
    """Extract charaters from the image of an erg screen

    This class implements the iterator protocol allowing
    the user to iterate through all charaters found in the image.
    It returns the charaters as SimpleImage. The iterator will also
    return newline (\n) and tab (\t) characters to represent spaces.

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
        self.im = Extractor.transform(im)

        # attributes for the iteration
        self.chpos = 0
        self.chars = Extractor.find_chars(self.im)

    @staticmethod
    def transform(im):
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
        bwdata = [0 if v <= Extractor.BW_THRESHOLD else 255 for v in list(transformed.getdata())]
        transformed.putdata(bwdata)

        # allow the user to rotate the image
        while True:
            print(SimpleImage(transformed.resize(Extractor.CONSOLE_SIZE, Image.BILINEAR)))
            rotate = int(input("Rotate: "))
            if (rotate == 0):
                break
            transformed = transformed.rotate(rotate, expand=True)

        # crop and resize it to its final size
        transformed = transformed.crop(Extractor.INITAL_CROP).resize(Extractor.FINAL_SIZE, Image.BILINEAR)

        # recompute the black and white data because rotation/resizing blurs it
        bwdata = [0 if v <= Extractor.BW_THRESHOLD else 255 for v in list(transformed.getdata())]
        transformed.putdata(bwdata)

        return transformed

    @staticmethod
    def find_chars(im):
        """Finds suspected charaters in the image

        Splits the image into lines and charaters based on white space.

        Args:
            im (Image): Pre-transformed (croped, b/w) image to extract from

        Returns:
            List of 4-tuples of the left, top, right, bottom coordinates
            of suspected charaters or '\n','\t' to represent new lines and spaces
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
                    if (switches < Extractor.SWITCH_THRESHOLD):
                        # remove small lines as they are probably garbage
                        if ((r-1) - top > 15):
                            lines.append((top, r-1))
                        inline = False
                else:
                    # if not in line but above threshold, entering a line
                    if (switches >= Extractor.SWITCH_THRESHOLD):
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
                of suspected charaters or '\n','\t' to represent new lines and spaces
            """
            chars = []

            # look through each line
            for top, bottom in lines:
                left = 0
                inchar = False
                blank = 0 # count blank lines

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
                        if (count < Extractor.BLACK_COUNT_THRESHOLD):

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
                        if (count >= Extractor.BLACK_COUNT_THRESHOLD):
                            inchar = True
                            left = c

                            # add an indicator if the spacing between charaters is large
                            if (blank >= 10):
                                chars.append('\t')

                            blank = 0
                        else:
                            blank += 1

                # add a new line indicator
                chars.append('\n')

            return chars

        pixels = [1 if v == 0 else 0 for v in list(im.getdata())]
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

        return get_chars(pixels, get_lines(pixels))

    @staticmethod
    def is_whitespace(item):
        """Determine whether an item returned from extration is whitespace

        Args:
            item (Object): item to test

        Returns:
            True iff the item is a newline or tab character
        """
        return item == '\n' or item == '\t'


    def __iter__(self):
        return self

    def next(self):
        """Returns the next item found in the image.

        Returns:
            Either '\n'/'\t' if the next item is whitespace or a SimpleImage
            if there is a digit.
        """
        # check that this is not the last line
        if (self.chpos < len(self.chars)):
            # check if it is a spacing charater or coordinates
            if (Extractor.is_whitespace(self.chars[self.chpos])):
                c = self.chars[self.chpos]
            else:
                # if its coordinates, crop the image anc create a SimpleImage
                c = SimpleImage(self.im.crop(self.chars[self.chpos]))
            # increment to the next charater
            self.chpos += 1
            return c
        else:
            raise StopIteration()
