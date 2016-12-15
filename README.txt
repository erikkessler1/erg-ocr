Erik Kessler
CSCI 373
Final Project: Erg Screen OCR

### ABOUT ###

  Machine learning system for reading pictures of Concept 2 Erg screens
  to return data from the image in a computer-usable form.

  The ML algorithm used is a kNN algorithm. You can specify k when running
  the algorithm.

  There are a pre-trained classifiers in the training_data directory. Although you
  could create your own classifier using the "train" command.

  There are images in the images directory to run the system on.

  Example:
  $ ./ergocr classify 3 training_data/lo_04.txt images/dataset1/04.jpg
     - When asked for the rotation put in 1 then 0
     - Compare the output to the image at "images/dataset1/04.jpg"

  Notes:
   - When the system asks you to rotate, you should try to make the bottom of the
     white box straight. Enter a rotation of 0 when done
   - If you don't have python installed at /usr/bin/python you can
     run by replacing "./ergocr" with  "python ergocr"

### TRAINING ###

  COMMAND:
    ./ergocr train <output-file> <training-image>

  DESCRIPTION:
    This will ask you to classify each character the system
    extracts and will store the data in the output-file.

    Notes:
     - For : and . you have to type ':' and '.'
     - You can skip classifying a digit with 's'

### CLASSIFYING ###

  COMMAND:
    ./ergocr classify [k=3] <classifier> <image>

  DESCRIPTION:
    This runs the ML algorithm on the image using the specified classifier.
    You can specify k, if unspecified, k=3.
