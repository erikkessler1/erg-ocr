import re

PATTERN = r"""Digit: (?P<digit>.)
File: (?P<file>.*)
(?P<data>[ #\n]*)
@
"""

def classify(classifier_path, image):
    """Classify an image

    Args:
        classifier_path (String): path to the classifier data
        image (SimpleImage): the image to classify

    Returns:
        The symbol that the classifier determines the image to be
    """
    # open the classifier
    with open(classifier_path, 'r') as f:
        text = f.read()

        # use regex to parse the data
        regex = re.compile(PATTERN)
        for match in regex.finditer(text):
            print match.group('data')
            print match.group('digit')
