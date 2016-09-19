import glob
import extract_utils
import progressbar
import csv

'''
EXTRACT.PY

Iterates through all .txt files found in the data directory, extracting the author and title from them
and saving this information (along with the file's path) to "textData.txt"

'''
globResults = glob.glob("./data/**/*.txt", recursive=True)

print("Found " + str(len(globResults)) + " texts.")

texts = []
authorSet = set()
dataNotFoundCount = 0

print("Extracting authors and titles from all texts...")

bar = progressbar.ProgressBar(max_value=len(globResults)-1)
# Iterate through all files in the data folder
# (Iterate by index for the progress bar counter)
for i in range(len(globResults)):

    if i % 100 == 0 or i == len(globResults)-1:
        bar.update(i)

    filename = globResults[i]

    fileData = extract_utils.get_lines_from_file(filename)

    if fileData is None:
        continue

    # Iterate through all lines until an author line is discovered
    # (Iterate by index to allow for searching around lines by index)
    authorFound = False
    titleFound = False
    title = ""
    authors = []
    for lineNumber in range(len(fileData)):
        line = fileData[lineNumber]

        # Identify line with author, and extract all authors
        if "Author: " in line:
            authors = extract_utils.extract_authors(line)
            authorFound = True
            # If all data has been found, stop searching through lines
            if titleFound:
                break

        # Identify line with title, and extract title
        if "Title: " in line:
            title = extract_utils.extract_title(line)
            titleFound = True
            # If all data has been found, stop searching through lines
            if authorFound:
                break

    # If either the author or title was not found, increment counter
    if not authorFound or not titleFound:
        dataNotFoundCount += 1
    else:
        texts.append((title, authors, filename))

print()
print("Missing data for " + str(dataNotFoundCount) + " texts (" +
      str(dataNotFoundCount * 100 / (len(globResults))) + "%)")


print()
print("Saving extracted info.txt to CSV file...")

with open('textData.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH'])

    for text in texts:
        csv_out.writerow(text)


