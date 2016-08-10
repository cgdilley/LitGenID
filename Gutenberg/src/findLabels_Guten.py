import findLabels_utils
import re
import csv
import progressbar
from bs4 import BeautifulSoup

# Gutenberg genres to filter by
genres = {'Adventure', 'Fantasy', 'Horror', 'Mystery Fiction', 'Western', 'Science Fiction', 'Crime Fiction',
          "Children's Myths, Fairy Tales, etc.", 'Love'}


print("Reading data from CSV file...")

data = []

# Open csv file containing text data
with open("../textData.txt", "r") as f:
    csvReader = csv.reader(f)
    # Iterate through all data rows
    for row in csvReader:
        datum = findLabels_utils.extract_data_from_row(row)
        if datum is not None:
            data.append(datum)


print("Finding texts in defined genres...")

outputData = []

bar = progressbar.ProgressBar(max_value=len(data)-1)

# Iterate through all data
for i in range(len(data)):
    bar.update(i)

    datum = data[i]

    # Ignoring texts in the "etext" folders
    if "etext" in datum.path:
        continue

    # Extract the gutenberg ebook ID# from the path
    textNumber = re.sub(r'.*/(\d+)(-.+)?\.txt', r'\1', datum.path)

    # Convert this number into a path in the catalog
    catalogPath = "../epub/{}/pg{}.rdf".format(textNumber, textNumber)
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
    for bookshelf in bookshelves:
        # Extract the bookshelf label
        value = bookshelf.find("value").contents[0]

        # If the label is within the set of genres
        if value in genres:
            # Add it to the list of output data
            outputData.append((datum.title, datum.authors, datum.path, value))

            # Progressively update the output csv file with each match
            with open('textDataWithGenre.txt', 'w') as out:
                csv_out = csv.writer(out)
                csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'GENRE'])

                for text in outputData:
                    csv_out.writerow(text)




