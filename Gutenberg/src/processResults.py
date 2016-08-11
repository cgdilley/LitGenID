import processResults_utils
import csv

'''
PROCESSRESULTS.PY

Merges the outputs from FINDLABELS_IBLIST.PY and FINDLABELS_GUTEN.PY, removing any duplicates after merging their
sets of genres, outputs CSV file of results to "./textData_FINAL.txt" and also outputs pretty human-readable summary
into "./genreCounts.txt".
'''

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

# Set of genres identified by Gutenberg catalog
gutenGenres = {'Adventure', 'Fantasy', 'Horror', 'Mystery Fiction', 'Western', 'Science Fiction', 'Crime Fiction',
               "Children's Myths, Fairy Tales, etc.", 'Love', 'Detective Fiction'}
# Set of genres identified by IBList
iblistGenres = {'Adventure', 'Crime and Mystery', 'Horror', 'Romance', 'Science Fiction', 'Western', 'Fantasy',
                'Mystery', 'Romance and Relationships', 'Fairy Tales', 'Love and Romance', 'Mystery and Detectives',
                'Science Fantasy', 'Futuristic', 'Time Travel', 'Dark Fantasy', 'Detectives and Horror'}


# Maps genres assigned by other sources to official genre identifiers
genreMapping = {'Adventure': ADVENTURE,
                'Fantasy': FANTASY,
                'Horror': HORROR,
                'Mystery Fiction': CRIME_MYSTERY,
                'Western': WESTERN,
                'Science Fiction': SCIENCE_FICTION,
                'Crime Fiction': CRIME_MYSTERY,
                "Children's Myths, Fairy Tales, etc.": FAIRY_TALE,
                'Love': ROMANCE,
                'Detective Fiction': CRIME_MYSTERY,

                'Crime and Mystery': CRIME_MYSTERY,
                'Romance': ROMANCE,
                'Mystery': CRIME_MYSTERY,
                'Romance and Relationships': ROMANCE,
                'Fairy Tales': FAIRY_TALE,
                'Love and Romance': ROMANCE,
                'Mystery and Detectives': CRIME_MYSTERY,
                'Science Fantasy': FANTASY,  # Sub-genre of Science Fiction
                'Futuristic': SCIENCE_FICTION,  # Sub-genre of Romance
                'Time Travel': SCIENCE_FICTION,  # Sub-genre of Romance and of Science Fiction
                'Dark Fantasy': FANTASY,  # Sub-genre of Horror AND of Fantasy... but points more towards Fantasy
                'Detectives and Horror': CRIME_MYSTERY,  # Sub-genre of Horror
                }

# Load genre-labelled text file that was output from FINDLABELS_GUTEN.PY
gutenData = processResults_utils.csv_to_text_data_list("./textDataWithGenre.txt")
# Load genre-labelled text file that was output from FINDLABELS_IBLIST.PY
iblistData = processResults_utils.csv_to_text_data_list("./textDataWithGenre2.txt")

print("GUTEN DATA SIZE = " + str(len(gutenData)))
print("IBLIST DATA SIZE = " + str(len(iblistData)))

# Merge data sets into single TextData list, eliminating and merging the genres of duplicates
data = processResults_utils.merge_data(gutenData, iblistData)

print("MERGED SIZE = " + str(len(data)))

# Write to the output csv file
with open('textData_FINAL.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'GENRE'])

    for text in data:
        # Map all rough genres to set of official genres
        mappedGenres = set()
        for label in text.labels:
            mappedGenres |= {genreMapping[label]}

        csv_out.writerow((text.title, text.authors, text.path, mappedGenres))


# Write pretty human-readable file about the contents of the data set
# ===================================================================

# Initialize dictionary of key-value pairs, with an official genre identifier as the key, and a list of all TextData
# objects in that genre as the value
genreLists = dict()

# Initialize all lists in the dictionary
for genre in officialGenres:
    genreLists[genre] = []

# Iterate through all TextData in the merged set
for datum in data:

    # Collect a set of rough genres that have been converted into their official genre equivalent
    mappedGenres = set()
    for label in datum.labels:
        mappedGenres |= {genreMapping[label]}

    # Add the TextData to the lists of each genre to which it belongs
    for label in mappedGenres:
        # genreLists[label].append(processResults_utils.TextData(datum.title, datum.authors, datum.path, mappedGenres))
        genreLists[label].append(datum)

# Write to file
with open("genreCounts.txt", "w") as f:

    f.write("TOTAL BOOK COUNT = " + str(len(data)))
    genreEntryTotal = 0
    for bookList in genreLists.values():
        genreEntryTotal += len(bookList)
    f.write("\nAVERAGE GENRES PER BOOK = " + format((genreEntryTotal / len(data)), '.2f'))
    f.write("\n======================================================")
    f.write("\nBOOK COUNT BY GENRE:\n----------------------------")
    for genre, bookList in sorted(genreLists.items(), key=lambda i: i[0]):
        f.write("\n" + genre + " = " + str(len(bookList)))
    f.write("\n======================================================\n")

    for genre, bookList in sorted(genreLists.items(), key=lambda i: i[0]):
        f.write("\n")
        f.write("\nGENRE: " + genre)
        f.write("\nCOUNT = " + str(len(bookList)))
        f.write("\n-----------------------------")
        for book in sorted(bookList, key=lambda b: b.title):
            f.write("\n" + str(book))
        f.write("\n")
