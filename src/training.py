from PIL import Image
from extract import Extractor
import os.path

CLASSIFIER_FORMAT = """Digit: {}
File: {}
{}
@
"""

def train(classifier_path, image_path):
    """Train the classifier with an image.

    This method extract digits from the image, then prompts the user
    to classify the image. That classification is stored in the following format:

    Digit: [classification]
    File: [image taken from]
    [PIXEL DATA]
    @

    Args:
        classifier_path (String): path to the file holding the classifier data
        image_path (String): path to the image to train on
    """

    # open the classifier file
    with open(classifier_path, "a+") as f:

        # open the image
        im_name = os.path.basename(image_path)
        im = Image.open(image_path)

        # create an Extractor
        e = Extractor(im)

        # iterate over the SimpleImages extracted
        for s_im in e:
            # chack that it isn't whitespace
            if (not Extractor.is_whitespace(s_im)):

                # print the image and have the user classify it
                print s_im
                digit = input("Input value: ")

                # write the data to the file
                f.write(CLASSIFIER_FORMAT.format(digit, im_name, str(s_im)))
