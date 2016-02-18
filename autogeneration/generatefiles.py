__author__ = 'giulio'

import re
import os
import csv
import sys

## Constants

NUM_ENTRIES = 8
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
        newPaper = (templateNewPaperRaw % tuple(orderedRows[i][-1][0:-3])).replace('currSection', orderedRows[i][1].replace(' ', ''))
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
        if not len(row) == 8:
            print 'Check entry:\n%s\n8 required arguments' % row
            sys.exit()

        # Add new paper to the current section
        newPaper = (templateNewPaperRaw % tuple(row[0:-3])).replace('currSection', sectionTitle.replace(' ', '')).replace('fileName', row[-3])

        # Remove parts not available
        if int(row[-1]) == 0:
            parts = newPaper.split('<!-- Poster -->\n')
            newPaper = parts[0] + parts[2]
        if int(row[-2]) == 0:
            parts = newPaper.split('<!-- Word cloud -->\n')
            newPaper = parts[0] + '<div>\n' + parts[2]
        if len(row[-3]) == 0:
            parts = newPaper.split('<!-- Links -->\n')
            newPaper = parts[0] + parts[2]
        elif row[-3][0:4] == 'http':
            parts = newPaper.split('<!-- Links -->')
            newPaper = parts[0] + r'<a class="btn light" href="%s"><i class="icon-doc" title="URL"></i>URL</a>' % row[-3] + parts[2]

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
        if not len(row) == 8:
            print 'Check entry:\n%s\n8 required arguments' % row
            sys.exit()

        # Add new paper to the current section
        newPaper = (templateNewPaperRaw % tuple(row[0:-3])).replace('currSection', sectionTitle.replace(' ', '')).replace('fileName', row[-3])

        publications.append(newPaper)

    # Add last section
    if not len(sectionTitle) == 0 and not len(publications) == 0:
        section.append((templateSectionRaw % ('\n'.join(publications))).replace('currSection', sectionTitle))

    return '\n'.join(section)

def fillPlaceholder(filePath, id, toInsert):
    fileToFill = open(filePath, 'rb').read()
    if filePath[-4:] == 'html':
        fileToFill = fileToFill.split('<!-- Automatic generated: %s -->' % id)
        fileFilled = fileToFill[0] + '<!-- Autogenerated: start-->\n' + toInsert + '<!-- Autogenerated: end -->\n' +  fileToFill[1]
    elif filePath[-3:] == 'tex':
        fileToFill = fileToFill.split(r'%' + ' Automatic generated: %s' % id)
        fileFilled = fileToFill[0] + r'%' + ' Autogenerated: start\n' + toInsert + r'%' + ' Autogenerated: end\n' +  fileToFill[1]
    return fileFilled

if __name__ == '__main__':

    # filenames
    pubsList = '/Users/giulio/Dropbox (Personal)/Giulio/Education/4_PhD/Publications/publications.csv'
    templatePubsSection = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/publicationsSection.html'
    templateNewPaperPublications = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/publicationsPaper.html'
    templateNewPaperIndex = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/indexPaper.html'
    templateIndex = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/index.html'
    templatePublications = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/publications.html'
    outPublications = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/publications.html'
    outIndex = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/index.html'
    
    # curriculum
    templateCv = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/giulio_marin_cv_tofill.tex'
    templatePubsCvSection = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/cvSection.tex'
    templateNewPaperCv = '/Users/giulio/Dropbox (Personal)/Giulio/Sites/current/autogeneration/cvPaper.tex'
    outCv = '/Users/giulio/Dropbox (Personal)/Giulio/Documents/Curriculum_Vitae/latex/giulio_marin_cv.tex'
    

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
    cvFilled = fillPlaceholder(templateCv, 'publications', publications)
    
    ## write files
    open(outIndex, 'w').write(indexFilled)
    print('File generated: %s' % outIndex)
    open(outPublications, 'w').write(publicationsFilled)
    print('File generated: %s' % outPublications)
    open(outCv, 'w').write(cvFilled)
    print('File generated: %s' % outCv)
