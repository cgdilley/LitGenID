import processResults_utils as Utils
import progressbar
import re
import codecs
import csv


# Official genres
ADVENTURE = 'Adventure'
FANTASY = 'Fantasy'
HORROR = 'Horror'
CRIME_MYSTERY = 'Crime and Mystery'
WESTERN = 'Western'
SCIENCE_FICTION = 'Science Fiction'
FAIRY_TALE = 'Fairy Tale'
ROMANCE = 'Romance'

# Put official genre constants into set
officialGenres = {ADVENTURE, FANTASY, HORROR, CRIME_MYSTERY, WESTERN, SCIENCE_FICTION, FAIRY_TALE, ROMANCE}

print("Loading CSV data...")

data = Utils.csv_to_text_data_list("./textData_FINAL.txt")

print("Building folder structure...")

Utils.make_sure_path_exists("./CORPUS/")

for genre in officialGenres:
    Utils.make_sure_path_exists(Utils.format_genre_path(genre))

print("Copying and trimming files to corpus directory...")

outputData = []

bar = progressbar.ProgressBar(max_value=len(data)-1)
for i in range(len(data)):
    if i % 20 == 0:
        bar.update(i)

    datum = data[i]

    # Extract the gutenberg ebook ID# from the path
    textNumber = re.sub(r'.*/(\d+)(-.+)?\.txt', r'\1', datum.path)

    # Open file with UTF-8
    f = codecs.open(datum.path, 'r', 'utf-8')

    # Attempt to read lines from the file
    try:
        lines = f.readlines()
    # If a Unicode decoding exception occurred, try to reopen using ISO-8859-1
    except UnicodeDecodeError:
        f.close()
        f = codecs.open(datum.path, 'r', 'iso-8859-1')
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

    # Initialize list of paths to store in catalog
    paths = []
    # Iterate through all genres associated with this TextData
    for genre in datum.labels:
        # Construct a path for this text and its genre
        newPath = Utils.format_genre_path(genre) + textNumber + ".txt"
        paths.append(newPath)
        # Open output file
        f = open(newPath, "w")

        # Write all lines to the file
        for line in outputLines:
            f.write(line)

        # Close output file
        f.close()

    # Add catalog entry to output list
    outputData.append((datum.title, datum.authors, paths, datum.labels))

bar.finish()

print("Outputting copied files to corpus catalog...")

# Write to the output csv file
with open('./CORPUS/catalog.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATHS', 'GENRE'])

    for text in outputData:
        csv_out.writerow(text)

print("Done!")
