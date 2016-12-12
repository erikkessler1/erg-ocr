import re

PATTERN = r"""Digit: (?P<digit>.)
File: (?P<file>.*)
(?P<data>[ #\n]*)
@
"""
regex = re.compile(PATTERN)

with open("../training_data.txt", 'r') as f:
    text = f.read()
    for match in regex.finditer(text):
        print match.group('data')
        print match.group('digit')
