# Update copyright information in html files

__author__ = 'giulio'

import re
import os
import csv
import sys
from datetime import date

COPYRIGHT_STRING = r'&#169;2012-%s&nbsp;<a href="%sindex.html">Giulio Marin</a>'
CURRENT_YEAR = date.today().year
MAIN_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

if __name__ == '__main__':
    for dirname, _, filenames in os.walk(MAIN_DIR):
        for filename in filenames:
            extension = os.path.splitext(filename)[1]
            if not (len(extension) > 0 and extension[1:] in ['html']):
                continue
            currFile = os.path.join(dirname, filename)
            fileContent = open(currFile, 'r').read()
            for prevFold in ['', '../', '../../']:
                for prevYear in range(0, 10):
                    fileContent = fileContent.replace(COPYRIGHT_STRING % (str(CURRENT_YEAR - prevYear), prevFold), COPYRIGHT_STRING % (str(CURRENT_YEAR), prevFold))
            open(currFile, 'w').write(fileContent)
            print 'File updated: %s' % os.path.relpath(os.path.join(dirname, filename), MAIN_DIR)
