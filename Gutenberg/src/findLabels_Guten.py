import findLabels_utils
import re
import csv
import progressbar
from bs4 import BeautifulSoup

'''
FINDLABELS_GUTEN.PY

Reads Title, Author, and Path data for each book from "textData.txt", queries Gutenberg catalog in ./epub/ directory
for the genre of each book, stores books that match at least one of the genres in the defined genre set, and writes
these books labelled with their appropriate genre into "textDataWithGenre.txt".

'''

# Gutenberg genres to filter by
genres = {'Adventure', 'Fantasy', 'Horror', 'Mystery Fiction', 'Western', 'Science Fiction', 'Crime Fiction',
          "Children's Myths, Fairy Tales, etc.", 'Love', 'Detective Fiction'}


print("Reading data from CSV file...")

data = findLabels_utils.csv_to_text_data_list("./textData.txt")

print("Finding texts in defined genres...")

outputData = []

bar = progressbar.ProgressBar(max_value=len(data)-1)

# Iterate through all data
for i in range(len(data)):
    if i % 20 == 0:
        bar.update(i)

    datum = data[i]

    # Ignoring texts in the "etext" folders
    if "etext" in datum.path:
        continue

    # Extract the gutenberg ebook ID# from the path
    textNumber = re.sub(r'.*/(\d+)(-.+)?\.txt', r'\1', datum.path)

    # Convert this number into a path in the catalog
    catalogPath = "./epub/{}/pg{}.rdf".format(textNumber, textNumber)
    try:
        # Attempt to open the catalog file at the path
        f = open(catalogPath)
    except FileNotFoundError:
        # If the file is not found, skip this data entry
        continue

    # Extract the contents of the file as an xml tree
    soup = BeautifulSoup(f.read(), "xml")

    # Close the file
    f.close()

    # Get all 'bookshelves' (genres) associated with this book
    bookshelves = soup.find_all("bookshelf")

    # Iterate through all found bookshelves
    genreMatches = []
    for bookshelf in bookshelves:
        # Extract the bookshelf label
        value = bookshelf.find("value").contents[0]

        # If the label is within the set of genres
        if value in genres:
            # Add it to the list of genre matches
            genreMatches.append(value)

    if len(genreMatches) > 0:
        outputData.append((datum.title, datum.authors, datum.path, genreMatches))

bar.finish()

# Write to the output csv file
with open('textDataWithGenre.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'GENRE'])

    for text in outputData:
        csv_out.writerow(text)




