import glob, codecs
import re
import guten_utils

globResults = glob.glob("./data/1/1/**/*.txt", recursive=True)

fileData = []
authorSet = set()

# Iterate through all files in the data folder
for filename in globResults:

    fileData = gu

    # Iterate through all lines until an author line is discovered
    for line in fileData:
        if "Author: " in line:
            newLine = line.replace("Author: ", "")
            authorSet |= {newLine}
            break


for author in sorted(authorSet):
    print(author)

