import re
from simple_image import SimpleImage

PATTERN = r"""Digit: (?P<digit>.)
File: (?P<file>.*)
(?P<data>[ #\n]*)
@
"""

def find_nearest(k, data):
    neighbors = sorted(data, key=lambda x: x[1], reverse=True)[:k]
    counts = {}
    for (d, _) in neighbors:
        counts[d] = counts.get(d, 0) + 1
    d, n = sorted(counts.items(), key=lambda x: x[1], reverse=True)[0]
    if (float(n)/k > 0.5):
        return d
    else:
        return neighbors[0][0]


def similarity(s_im1, s_im2):
    """Determine the similarity of two simple images.

    Returns:
        An int representing the similarity of the images
    """
    count = 0
    pxls1 = s_im1.pixels
    pxls2 = s_im2.pixels

    for i in range(0, len(pxls1)):
        for j in range(0, len(pxls1[i])):
            try:
                p1 = pxls1[i][j]
                p2 = pxls2[i][j]
                if (p1 == p2):
                    count += 1
            except:
                pass
    return count

def classify(k, classifier_path, image):
    """Classify an image

    Args:
        k (Int): how many neighbors to look at
        classifier_path (String): path to the classifier data
        image (SimpleImage): the image to classify

    Returns:
        The symbol that the classifier determines the image to be
    """
    def find_sim(template_data, image):
        """Computes the similarity between the template and the image.

        Args:
            template_data (Match): regex match that holds the 'data' and 'digit'
            image (Image): the image to compare to

        Returns:
            A tuple of the classification and the similarity.
        """
        template = SimpleImage.fromString(template_data.group('data'))
        classification = match.group('digit')
        return (classification, similarity(template, image))

    # open the classifier
    with open(classifier_path, 'r') as f:
        text = f.read()

        # use regex to parse the data
        regex = re.compile(PATTERN)

        # print the nearest neighbor
        print findNearest(k, [find_sim(match, image) for match in regex.finditer(text)])
