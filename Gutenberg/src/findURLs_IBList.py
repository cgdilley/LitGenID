import findLabels_utils
import csv
import progressbar
from numpy import random

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

'''
authorSet = set()
for datum in data:
    authorSet |= {datum.authors[0]}

for author in sorted(authorSet):
    print(author)

quit()
'''

print()
print("Searching iblist.com for matches:")
print("--------------------")

data = sorted(data, key=lambda d: d.title)

outputData = []
foundCount = 0
bar = progressbar.ProgressBar(max_value=len(data))
for i in range(len(data)):
    if i % 10 == 0 or i == len(data) - 1:
        bar.update(i)

    datum = data[i]

    resultUrl = findLabels_utils.perform_search(datum)
    if resultUrl is not None:
        result = (datum.title, datum.authors, datum.path, resultUrl)
        outputData.append(result)
        with open('textDataWithURL.txt', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['TITLE', 'AUTHOR', 'FILEPATH', 'BOOKURL'])

            for text in outputData:
                csv_out.writerow(text)
    else:
        with open('rejectedTitles.txt', 'a') as out:
            out.write(datum.title + " --- " + datum.authors[0] + "\n")

print("--------------------")
print()
print("Saving extracted info to CSV file...")








