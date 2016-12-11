Erik Kessler
CSCI 373
Final Project: Erg Screen OCR

### ABOUT ###

  Machine learning system for reading pictures of Concept 2 Erg screens
  to return data from the image in a computer-usable form.

  The ML algorithm used is a kNN algorithm. You can specify k when running
  the algorithm.

  There is a pre-trained classifier in training_data.txt. Although you
  could create your own classifier using the "train" command.

  There are test images in "/images/test/" to test the system on.

  Note: if you don't have python installed at /usr/bin/python you can
        run by replacing "./ergocr" with  "python ergocr"

### TRAINING ###

  COMMAND:
    ./ergocr train <output-file> <training-image>

  DESCRIPTION:
    This will ask you to classify each character the system
    extracts and will store the data in the output-file

### READING ###

  COMMAND:
    ./ergocr read [k=3] <classifier> <image>

  DESCRIPTION:
    This runs the ML algorithm on the image using the specified classifier.
    You can specify k, if unspecified, k=3.
