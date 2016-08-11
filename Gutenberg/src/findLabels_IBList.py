import findLabels_utils
import progressbar
import csv

'''
FINDLABELS_IBLIST.PY

Reads Title, Author, Path, and URL data from "textDataWithURL.txt", queries the associated URL, extracts the genre
from the received HTML, attaches it the title/author/path data, and writes the results to "textDataWithGenre2.txt"
'''

# Set of all genres from IBList to accept
genreSet = {'Adventure', 'Crime and Mystery', 'Horror', 'Romance', 'Science Fiction', 'Western', 'Fantasy',
            'Mystery', 'Romance and Relationships', 'Fairy Tales', 'Love and Romance', 'Mystery and Detectives',
            'Science Fantasy', 'Futuristic', 'Time Travel', 'Dark Fantasy', 'Detectives and Horror'}

# Open csv file containing text data
data = findLabels_utils.csv_to_text_data_list("./textDataWithURL.txt")

outputData = []

bar = progressbar.ProgressBar(max_value=len(data)-1)

# Iterate through all data entries
for i in range(len(data)):
    if i % 10 == 0:
        bar.update(i)

    datum = data[i]

    # Query the URL associated with the data element, and extract the genre information from HTML reply
    genres = findLabels_utils.extract_iblist_genres(datum.url, genreSet)

    # If at least one genre was identified
    if len(genres) > 0:
        # Remove duplicates
        genres = list(set(genres))
        # Add result to output list
        outputData.append((datum.title, datum.authors, datum.path, genres))

bar.finish()

# Write to the output csv file
with open('textDataWithGenre2.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'GENRE'])

    for text in outputData:
        csv_out.writerow(text)

