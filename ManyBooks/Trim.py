import re
import codecs
import os
import glob


os.chdir("genres/")
for filename in glob.glob("*/*.txt"):
    f = codecs.open(filename, 'r', 'latin-1')
    print("reading file")
    try:
        lines = f.readlines()
    # If a Unicode decoding exception occurred, try to reopen using ISO-8859-1
    except UnicodeDecodeError:
        f.close()
        f = codecs.open(filename, 'r', 'latin-1')
        lines = f.readlines()

    # Close input file
    f.close()

    # Set default start and end lines for the text
    startMarker = 0
    endMarker = len(lines)

    # Search for START and END tags for the text, and adjust the markers accordingly
    for lineNum in range(len(lines)):
        line = lines[lineNum]
        if re.search(r'\*+ ?START OF TH', line):
            startMarker = lineNum + 1
        if re.search(r'\*+ ?END OF TH', line):
            endMarker = lineNum - 4
            break

    # Take only the lines within the markers
    outputLines = lines[startMarker:endMarker]

    # Open output file
    f = codecs.open(filename, 'w', 'latin-1')
    print("writing file")

    # Write all lines to the file
    for line in outputLines:
        f.write(line)

    # Close output file
    f.close()
