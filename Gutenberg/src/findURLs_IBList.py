import findLabels_utils
import csv
import progressbar

'''
FINDURLS_IBLIST.PY

Reads Title, Author, and Path data for each book from "textData.txt", queries iblist.com for each book and stores
the URL of the book match, and writes all results to "textDataWithURL.txt" to be further processed
by FINDLABELS_IBLIST.PY in order to acquire genre label.
'''

print("Reading data from CSV file...")


# Open csv file containing text data
data = findLabels_utils.csv_to_text_data_list("./textData.txt")

# Open csv file containing already-extracted data
outputData = findLabels_utils.csv_to_text_data_list("./textDataWithURL.txt")
outputData = [(datum.title, datum.authors, datum.path, datum.url) for datum in outputData]

try:
    with open("./saveMarker.txt", "r") as f:
        startIndex = int(f.read())
except FileNotFoundError:
    startIndex = 0


print()
print("Searching iblist.com for matches:")
print("--------------------")

print("Starting from index " + str(startIndex))

data = sorted(data, key=lambda d: d.title)

foundCount = 0
bar = progressbar.ProgressBar(max_value=len(data)-startIndex-1)
# Iterate through all data elements
for i in range(startIndex, len(data)):
    if i % 20 == 0:
        bar.update(i-startIndex)
        # Update progress marker
        with open("./saveMarker.txt", "w") as f:
            f.write(str(i))
        # Update output file
        with open('./textDataWithURL.txt', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'BOOKURL'])
            for text in outputData:
                csv_out.writerow(text)

    datum = data[i]

    # Search for the given book/author on IBList, and get URL of result (if found)
    resultUrl = findLabels_utils.perform_iblist_search(datum)

    # If the result was found
    if resultUrl is not None:
        # Add the result to the results list
        result = (datum.title, datum.authors, datum.path, resultUrl)
        outputData.append(result)

bar.finish()

print("--------------------")
print()
print("Saving extracted info to CSV file...")

# Update progress marker
with open("./saveMarker.txt", "w") as f:
    f.write(str(len(data)))
# Update output file
with open('./textDataWithURL.txt', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'BOOKURL'])
    for text in outputData:
        csv_out.writerow(text)








