import numpy as np
import math
import matplotlib.pyplot as plt
import csv

"""
GENRE_RESULTS.PY
This script reads a matrix (in text form) from the text file 'matrix.txt', converts it into a proper confusion matrix,
and performs accuracy, precision, recall, f1-score calculations on every label, as well as generating their 1-vs-all
confusion matrices.
"""

# Path to corpus files
TEXT_DATA_DIR = "./Corpus/PROCESSED/"
# Path to the labels index
LABEL_INDEX_FILE = TEXT_DATA_DIR + "labels_proper.txt"

# Genres to include in training (usually [0, 1, 2, 3, 4, 5, 6, 7])
GENRES_TO_USE = [0, 1, 2, 3, 4, 5, 6, 7]
# It is important to ensure that this list is sorted
GENRES_TO_USE = sorted(GENRES_TO_USE)


label_index = dict()

# Load label index CSV
print("Loading label index...")
with open(LABEL_INDEX_FILE, "r") as f:
    csv_in = csv.reader(f)

    for row in csv_in:
        if row[0] != "LABEL":
            label_index[int(row[1])] = row[0]

# Read the matrix text file
with open("matrix.txt", "r") as f:
    input_str = f.read()

# Remove the beginning and ending brackets
input_str = input_str[1:-1]

matrix = []
line = []
number = []
# Read the file character by character, assembling the matrix along the way
for char in input_str:
    if char == "[":
        line = []
    if len(number) > 0 and char == " ":
        number = [math.pow(10, len(number) - x - 1) * number[x] for x in range(len(number))]
        line.append(int(sum(number)))
        number = []
    if char.isdigit():
        number.append(int(char))
    if char == "]":
        number = [math.pow(10, len(number) - x - 1) * number[x] for x in range(len(number))]
        line.append(int(sum(number)))
        number = []
        matrix.append(line)

# Count the number of genres in the given matrix
numGenres = len(matrix)

# Output the resulting matrix (to ensure that it matches the input)
for row in range(numGenres):
    line = ("[[  " if row == 0 else " [  ")
    for column in range(numGenres):
        if column > 0:
            int_digits = 0 if matrix[row][column] == 0 else int(math.floor(math.log10(matrix[row][column])))
            for i in range(1 + 4 - int_digits):
                line += " "
        line += str(matrix[row][column])
    line += "]" if row < numGenres-1 else "]]"
    print(line)

# Iterate through all genres/labels in the matrix
print("Genres count = %s" % numGenres)
for genre in range(numGenres):

    # Initialize counts for true positives, true negatives, false positives, and false negatives
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    # Iterate through all rows and columns
    for x in range(numGenres):
        for y in range(numGenres):
            if x == y == genre:     # If it's the row and column of the genre we're looking at, add true positives
                tp += matrix[x][y]
            elif x == genre:        # If its the column of the genre but not the row, false positive
                fp += matrix[x][y]
            elif y == genre:        # If its the row of the genre but not the column, false negative
                fn += matrix[x][y]
            else:                   # Otherwise, true negative
                tn += matrix[x][y]

    # Perform calculations based on true/false positive/negative counts
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = 0 if tp + fp == 0 else tp / (tp + fp)
    recall = 0 if tp + fn == 0 else tp / (tp + fn)
    f1 = 0 if precision + recall == 0 else 2 * ((precision * recall) / (precision + recall))

    # Assemble one-versus-all confusion matrix
    cm = [[tp, fn], [fp, tn]]

    # Output results
    print("\nGENRE %d\n------------" % genre)
    print("Accuracy = %f" % accuracy)
    print("Precision = %f" % precision)
    print("Recall = %f" % recall)
    print("F1 Score = %f" % f1)
    print("Confusion Matrix = %s" % str(cm))

# Find the largest value in the matrix, for normalization (and its number of digits)
cm_max = max([max(x) for x in matrix])
cm_max_log = int(math.floor(math.log10(cm_max)))

# PRINT PRETTY CONFUSION MATRIX PLOTS

# Get labels for genres
sorted_label_list = [label_index[x] for x in GENRES_TO_USE]

# Create a "normalized" version of the confusion matrix, ensuring all values fall in the range [0,1]
# Also, scales smaller values slightly so that they are more easily seen against null values
cm_normalized = [[math.pow(val/cm_max, 0.8) for val in row] for row in matrix]


def plot_text():
    """
    Plots text over each square in the confusion matrix representing the count of that square
    :return:  None
    """

    for x in range(numGenres):
        for y in range(numGenres):
            # Ignore printing 0-values
            val = matrix[y][x]
            if val == 0:
                continue

            # Get the normalized value of this square in order to determine text color
            norm_val = cm_normalized[y][x]

            plt.text(x, y, val, color="black" if norm_val < 0.7 else "white",
                     horizontalalignment="center", verticalalignment="center")

# Construct non-normalized confusion matrix plot
fig = plt.figure(1)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Greens)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(numGenres)
plt.xticks(tick_marks, sorted_label_list, rotation=45)
plt.yticks(tick_marks, sorted_label_list)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plot_text()
fig.patch.set_facecolor("white")

# Construct normalized confusion matrix plot
fig = plt.figure(2)
plt.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Greens)
plt.title("Normalized Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(numGenres)
plt.xticks(tick_marks, sorted_label_list, rotation=45)
plt.yticks(tick_marks, sorted_label_list)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plot_text()
fig.patch.set_facecolor("white")

# Output plots
plt.show()

