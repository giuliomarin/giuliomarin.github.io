__author__ = 'giulio'

import re
import os
import csv
import sys

## Constants

NUM_ENTRIES = 11
NUM_PUBLICATIONS_INDEX = 5

## Functions

def addPublicationsToIndex(templateNewPaper, pubslistPath):
    # Open template files
    templateNewPaperRaw = open(templateNewPaper, 'r').read()

    # Parse publications
    rows = csv.reader(open(pubslistPath, 'rb'), delimiter = ',')

    # Order by year
    unorderedRows = []
    newSection = False
    sectionTitle = ''
    for row in rows:
        # New section
        if len(row) == 0:
            sectionTitle = ''
            newSection = True
            continue
        # Save section title
        if newSection:
            sectionTitle = row[0]
            newSection = False
            rows.next()
            continue
        # Check to have all the fields
        if not len(row) == NUM_ENTRIES:
            print 'Check entry:\n%s\n%d required arguments' % (row, NUM_ENTRIES)
            sys.exit()

        unorderedRows.append([int(row[4]), sectionTitle, row])

    orderedRows = sorted(unorderedRows, key = lambda year: year[0], reverse = True)

    # Add most recent papers
    publications = []
    for i in range(0, NUM_PUBLICATIONS_INDEX):
        newPaper = (templateNewPaperRaw % tuple(orderedRows[i][-1][0:5])).replace('currSection', orderedRows[i][1].replace(' ', ''))
        publications.append(newPaper)

    return '\n\n'.join(publications)

def getNumberPublications(pubslistPath):
    # Parse publications
    rows = csv.reader(open(pubslistPath, 'rb'), delimiter = ',')

    # Count publications
    numPublications = 0
    for row in rows:
        # New section
        if len(row) == 0:
            rows.next()
            rows.next()
            continue
        numPublications += 1

    return numPublications

def addPublicationsToPublications(templateSection, templateNewPaper, pubslistPath):
    # Open template files
    templateSectionRaw = open(templateSection, 'r').read()
    templateNewPaperRaw = open(templateNewPaper, 'r').read()

    # Parse publications
    rows = csv.reader(open(pubslistPath, 'rb'), delimiter = ',')
    newSection = False
    sectionTitle = ''
    publications = []
    section = []

    for row in rows:
        # New section
        if len(row) == 0:
            # Previous section done
            if not len(sectionTitle) == 0 and not len(publications) == 0:
                section.append((templateSectionRaw % ('\n'.join(publications))).replace('currSection', sectionTitle))
                sectionTitle = ''
                publications = []
            newSection = True
            continue
        # Save section title
        if newSection:
            sectionTitle = row[0]
            newSection = False
            rows.next()
            continue

        # Check to have all the fields
        if not len(row) == NUM_ENTRIES:
            print 'Check entry:\n%s\n%d required arguments' % (row, NUM_ENTRIES)
            sys.exit()

        # Add new paper to the current section
        newPaper = (templateNewPaperRaw % tuple(row[0:5])).replace('currSection', sectionTitle.replace(' ', '')).replace('fileName', row[5])

        # Remove parts not available
        if int(row[7]) == 0: # no PDF
            parts = newPaper.split('<!-- Links -->\n')
            newPaper = parts[0] + '<!-- Links -->' + '\n  <!-- Links -->\n' + parts[2]
        if int(row[8]) == 0:  # no BIB
            parts = newPaper.split('<!-- Bib -->\n')
            newPaper = parts[0] + '<!-- Bib -->' + '\n  <!-- Bib -->\n' + parts[2]
        if row[10].startswith('http'): # add URL
            parts = newPaper.split('<!-- Links -->')
            newPaper = parts[0] + '<!-- Links -->' + parts[1] + r'  <a class="btn light" href="%s"><i class="icon-doc" title="URL"></i>URL</a>' % row[10] + '\n  <!-- Links -->' + parts[2]
        if int(row[9]) == 0: # no poster
            parts = newPaper.split('<!-- Poster -->\n')
            newPaper = parts[0] + parts[2]
        if int(row[6]) == 0: # no word cloud
            parts = newPaper.split('<!-- Word cloud -->\n')
            newPaper = parts[0] + '<div>\n' + parts[2]

        publications.append(newPaper)

    # Add last section
    if not len(sectionTitle) == 0 and not len(publications) == 0:
        section.append((templateSectionRaw % ('\n'.join(publications))).replace('currSection', sectionTitle))

    return '\n'.join(section)

def addPublicationsToCv(templateSection, templateNewPaper, pubslistPath):
    # Open template files
    templateSectionRaw = open(templateSection, 'r').read()
    templateNewPaperRaw = open(templateNewPaper, 'r').read()
    if templateNewPaperRaw[-1:] == '\n':
        templateNewPaperRaw = templateNewPaperRaw[0:-1]

    # Parse publications
    rows = csv.reader(open(pubslistPath, 'rb'), delimiter = ',')
    newSection = False
    sectionTitle = ''
    publications = []
    section = []

    for row in rows:
        # New section
        if len(row) == 0:
            # Previous section done
            if not len(sectionTitle) == 0 and not len(publications) == 0:
                section.append((templateSectionRaw % ('\n'.join(publications))).replace('currSection', sectionTitle))
                sectionTitle = ''
                publications = []
            newSection = True
            continue
        # Save section title
        if newSection:
            sectionTitle = row[0]
            newSection = False
            rows.next()
            continue

        # Check to have all the fields
        if not len(row) == NUM_ENTRIES:
            print 'Check entry:\n%s\n%d required arguments' % (row, NUM_ENTRIES)
            sys.exit()

        # Add new paper to the current section
        newPaper = (templateNewPaperRaw % tuple(row[0:5])).replace('currSection', sectionTitle.replace(' ', '')).replace('fileName', row[5])

        publications.append(newPaper)

    # Add last section
    if not len(sectionTitle) == 0 and not len(publications) == 0:
        section.append((templateSectionRaw % ('\n'.join(publications))).replace('currSection', sectionTitle))

    return '\n'.join(section)

def fillPlaceholder(filePath, id, toInsert):
    fileToFill = open(filePath, 'rb').read()
    if filePath.endswith('html'):
        fileToFill = fileToFill.split('<!-- Automatic generated: %s -->' % id)
        fileFilled = fileToFill[0] + '<!-- Autogenerated: start-->\n' + toInsert + '<!-- Autogenerated: end -->\n' +  fileToFill[1]
    elif filePath.endswith('tex'):
        fileToFill = fileToFill.split(r'%' + ' Automatic generated: %s' % id)
        fileFilled = fileToFill[0] + r'%' + ' Autogenerated: start\n' + toInsert + r'%' + ' Autogenerated: end\n' +  fileToFill[1]
    return fileFilled

if __name__ == '__main__':

    # Current path
    websitePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    # filenames
    pubsList = '/Users/giulio/Dropbox/Giulio/Education/7_Publications/publications.csv'
    templatePubsSection = os.path.join(websitePath, 'autogeneration/publicationsSection.html')
    templateNewPaperPublications = os.path.join(websitePath, 'autogeneration/publicationsPaper.html')
    templateNewPaperIndex = os.path.join(websitePath, 'autogeneration/indexPaper.html')
    templateIndex = os.path.join(websitePath, 'autogeneration/index.html')
    templatePublications = os.path.join(websitePath, 'autogeneration/publications.html')
    outPublications = os.path.join(websitePath, 'publications.html')
    outIndex = os.path.join(websitePath, 'index.html')

    # curriculum
    templatePubsCvSection = os.path.join(websitePath, 'autogeneration/cvSection.tex')
    templateNewPaperCv = os.path.join(websitePath, 'autogeneration/cvPaper.tex')
    outCv = '/Users/giulio/Documents/curriculum_vitae/latex/giulio_marin_cv_pub.tex'


    ## Add publications

    # index
    publications = addPublicationsToIndex(templateNewPaperIndex, pubsList)
    indexFilled = fillPlaceholder(templateIndex, 'publications', publications)

    # publications
    publications = addPublicationsToPublications(templatePubsSection, templateNewPaperPublications, pubsList)
    publicationsFilled = fillPlaceholder(templatePublications, 'publications', publications)
    numPublications = getNumberPublications(pubsList)
    publicationsFilled = publicationsFilled.replace('Number of publications: xxx', 'Number of publications: %d' % numPublications)

    # curriculum
    publications = addPublicationsToCv(templatePubsCvSection, templateNewPaperCv, pubsList)

    ## write files
    open(outIndex, 'w').write(indexFilled)
    print('File generated: %s' % outIndex)
    open(outPublications, 'w').write(publicationsFilled)
    print('File generated: %s' % outPublications)
    open(outCv, 'w').write(publications)
    print('File generated: %s' % outCv)
