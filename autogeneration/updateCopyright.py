# Update copyright information in html files

__author__ = 'giulio'

import re
import os
import csv
import sys
from datetime import date

COPYRIGHT_STRING = r'<p>&#169;%s&nbsp;<a href="index.html">Giulio Marin</a></p>'
CURRENT_YEAR = date.today().year

if __name__ == '__main__':
    for dirname, _, filenames in os.walk('/Users/giulio/Dropbox (Personal)/Giulio/Sites/current'):
        for filename in filenames:
            extension = os.path.splitext(filename)[1]
            if not (len(extension) > 0 and extension[1:] in ['html']):
                continue
            currFile = os.path.join(dirname, filename)
            fileContent = open(currFile, 'r').read()
            fileContent = fileContent.replace(COPYRIGHT_STRING % str(CURRENT_YEAR-1), COPYRIGHT_STRING % CURRENT_YEAR)
            open(currFile, 'w').write(fileContent)
            print 'File updated: %s' % filename
        