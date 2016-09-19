from keras.layers import Dense, Flatten
from keras.layers import Convolution1D, MaxPooling1D, Embedding
from keras.models import Sequential
from keras.utils.np_utils import to_categorical
import sklearn.metrics as sklm
from sklearn.cross_validation import StratifiedKFold
import os
import math
import time
import csv
import progressbar
import numpy as np
import matplotlib.pyplot as plt

"""
CNN.PY
This script is designed to read the files created by EMBED.PY and fit them to a convolutional neural network model.
"""

# Number of folds to split data into for cross-validation
FOLDS = 10
# Number of folds to actually test (only < FOLDS for debugging)
FOLDS_TO_USE = 1
# Epochs per fold
NUM_EPOCHS = 1
# Vector-length of GloVe vectors to use
VECTOR_SIZE = 50
# Number of words per document
MAX_SEQUENCE_LENGTH = 12000
# Number of texts per genre to limit the data set to (0 = no limit)
GENRE_MAX = 0

# Path to GloVe vector file
GLOVE_PATH = "./glove.6B/glove.6B."+str(VECTOR_SIZE)+"d.txt"
# Path to corpus files
TEXT_DATA_DIR = "./Corpus/PROCESSED/"
# Path to the word index
WORD_INDEX_FILE = TEXT_DATA_DIR + "index.txt"
# Path to the labels index
LABEL_INDEX_FILE = TEXT_DATA_DIR + "labels.txt"
# Path to the info file
INFO_FILE = TEXT_DATA_DIR + "info.txt"

# Genres to include in training (usually [0, 1, 2, 3, 4, 5, 6, 7])
GENRES_TO_USE = [0, 1, 2, 3, 4, 5, 6, 7]
# It is important to ensure that this list is sorted
GENRES_TO_USE = sorted(GENRES_TO_USE)
# Number of genres included in training
NUM_GENRES = len(GENRES_TO_USE)

# DICTIONARY CONSTANTS
ACC = "acc"
PREC = "prec"
REC = "rec"
F1S = "f1s"
CMX = "cmx"

# Load data

print("LOADING DATA FROM FILES...\n----------------------------------")

word_index = dict()
label_index = dict()

# Load word index CSV
print("Loading word index...")
with open(WORD_INDEX_FILE, "r") as f:
    csv_in = csv.reader(f)

    for row in csv_in:
        if row[0] != "WORD":
            word_index[row[0]] = int(row[1])

# Load label index CSV
print("Loading label index...")
with open(LABEL_INDEX_FILE, "r") as f:
    csv_in = csv.reader(f)

    for row in csv_in:
        if row[0] != "LABEL":
            label_index[int(row[1])] = row[0]

print("Loading data files...")

data = []
labels = []

# Iterate through all folders in the corpus directory
# These folders represent the different labels
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    if os.path.isdir(path):

        # If this folder's label is not on the list of genres to use, ignore it
        if int(name) not in GENRES_TO_USE:
            continue

        # Get list of all files in the directory
        genreFiles = sorted(os.listdir(path))

        time.sleep(0.005)  # So that this print statement doesn't mess with the progress bar
        print("Loading genre %s:" % label_index[int(name)])
        time.sleep(0.005)  # So that this print statement doesn't mess with the progress bar

        # Initialize progress bar for this genre
        if GENRE_MAX > 0:
            bar = progressbar.ProgressBar(max_value=min(len(genreFiles), GENRE_MAX))
        else:
            bar = progressbar.ProgressBar(max_value=len(genreFiles))

        # For iteration, keep track of unused files to better reflect the number of texts actually included
        nontextFileCount = 0
        # Iterate through all files in the labelled folder
        for findex in range(len(genreFiles)):
            fname = genreFiles[findex]

            # If we've reached the genre text limit, break the for loop
            if 0 < GENRE_MAX <= (findex - nontextFileCount):
                break

            bar.update(findex)

            # If we're looking at a text file, load it
            if ".txt" in fname:
                fpath = os.path.join(path, fname)
                # Open the file
                f = open(fpath)
                # Split into an array of tokens
                tokens = f.read().split(" ")
                # Convert this token array into a numpy array of integers, and then limit by MAX_SEQUENCE_LENGTH
                # Then append to the data list (the X list)
                data.append(np.array(tokens, np.int32)[:MAX_SEQUENCE_LENGTH])
                # Close the file
                f.close()

                # Add the label associated with this text to the label list (the Y list)
                labels.append(int(name))
            else:
                # Increment counter of non-text files
                nontextFileCount += 1
        bar.finish()

# Convert list into numpy array
data = np.array(data)

# Convert labels number into their index value in genres-to-use list, so that to_categorical() only includes
# labels that should be included.  When all genres are being used, this should change nothing.
labels = [GENRES_TO_USE.index(x) for x in labels]

# Create the k-fold cross validation info
kFold = StratifiedKFold(labels, FOLDS)

# Convert label array to categorical format
labels = to_categorical(np.asarray(labels))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

print("\nLOADING EMBEDDING VECTORS...\n--------------------------------")

# Load embeddings vectors
embeddings_index = {}
f = open(GLOVE_PATH)
lines = f.readlines()
bar = progressbar.ProgressBar(max_value=len(lines))
for i in range(len(lines)):
    bar.update(i)
    line = lines[i]

    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype="float32")
    embeddings_index[word] = coefs
f.close()
bar.finish()

time.sleep(0.005)  # So that this print statement doesn't mess with the progress bar
print("Found %s word vectors." % len(embeddings_index))
print("Building embedding matrix...")

# Create an embeddings matrix from the word index and the loaded embeddings
embedding_matrix = np.zeros((len(word_index) + 1, VECTOR_SIZE))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector


def build_model():
    """
    Function for building the machine learning model
    :return: The constructed model
    """
    # Define the machine learning model
    m = Sequential()
    # Convert the input into corresponding embeddings
    m.add(Embedding(len(word_index) + 1,
                    VECTOR_SIZE,
                    weights=[embedding_matrix],
                    input_length=MAX_SEQUENCE_LENGTH,
                    trainable=False))
    # Convolutional layer (16x32)
    m.add(Convolution1D(16, 32, activation="relu"))
    # Max-pooling layer (8-fold)
    m.add(MaxPooling1D(8))
    # Flatten convolutional output for dense layers
    m.add(Flatten())
    # Dense layer with 128 outputs
    m.add(Dense(128, activation="relu"))
    # Final output layer with as many outputs as genres
    m.add(Dense(NUM_GENRES, activation="softmax"))

    # Compile the model
    m.compile(loss="categorical_crossentropy",
              optimizer="rmsprop",
              metrics=["accuracy"])

    return m

# Use the above-defined function to construct the model
model = build_model()

print("\nFITTING MODEL...\n---------------------------------------")

results = []
counter = 0

# Iterate through all k-folds
for trn_i, test_i in kFold:

    counter += 1
    # If we've already run as many folds as are desired, break the for loop
    if counter > FOLDS_TO_USE:
        break

    print("Fold #" + str(counter) + ":")
    print("------------------")
    # Train the model
    model.fit(data[trn_i], labels[trn_i], nb_epoch=NUM_EPOCHS)
    # Test the model and get its predictions for the testing set
    predictions = model.predict(data[test_i])
    # Convert probabilistic predictions into concrete, absolute predictions
    predictions = np.array([[(0 if val != np.argmax(y) else 1) for val in range(NUM_GENRES)] for y in predictions])

    # Compare predictions with true values to get accuracy, precision, recall, and f1 score,
    # and build a confusion matrix
    accuracy = sklm.accuracy_score(labels[test_i], predictions)
    precision = sklm.precision_score(labels[test_i], predictions, average="macro")
    recall = sklm.recall_score(labels[test_i], predictions, average="macro")
    f1score = sklm.f1_score(labels[test_i], predictions, average="macro")
    matrix = sklm.confusion_matrix([np.argmax(y) for y in labels[test_i]], [np.argmax(y) for y in predictions])

    results.append(dict({ACC: accuracy, PREC: precision, REC: recall, F1S: f1score, CMX: matrix}))

    # Output results
    print("Accuracy = " + str(accuracy))
    print("Precision = " + str(precision))
    print("Recall = " + str(recall))
    print("F1 Score = " + str(f1score))
    print("Confusion Matrix = \n" + str(matrix))
    print()

    # Reset the model for next fold
    model = build_model()

print("\nFINAL RESULTS:\n===================")
print("Accuracy = " + str(np.mean([x[ACC] for x in results])))
print("Precision = " + str(np.mean([x[PREC] for x in results])))
print("Recall = " + str(np.mean([x[REC] for x in results])))
print("F1-Score = " + str(np.mean([x[F1S] for x in results])))


# Sum together all confusion matrices
cm = [[sum([r[CMX][x][y] for r in results]) for y in range(NUM_GENRES)] for x in range(NUM_GENRES)]
cm_max = max([max(x) for x in cm])

print("Overall confusion matrix = ")

# Print the confusion matrix to the console in a readable format
cm_max_log = int(math.floor(math.log10(cm_max)))
for row in range(NUM_GENRES):
    line = ("[[  " if row == 0 else " [  ")
    for column in range(NUM_GENRES):
        if column > 0:
            int_digits = 0 if cm[row][column] == 0 else int(math.floor(math.log10(cm[row][column])))
            for i in range(1 + cm_max_log - int_digits):
                line += " "
        line += str(cm[row][column])
    line += "]" if row < NUM_GENRES-1 else "]]"
    print(line)

# PRINT PRETTY CONFUSION MATRIX PLOTS


# Get labels for genres
sorted_label_list = [label_index[x] for x in GENRES_TO_USE]

# Create a "normalized" version of the confusion matrix, ensuring all values fall in the range [0,1]
# Also, scales smaller values slightly so that they are more easily seen against null values
cm_normalized = [[math.pow(val/cm_max, 0.8) for val in row] for row in cm]

# Construct non-normalized confusion matrix plot
plt.figure(1)
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(NUM_GENRES)
plt.xticks(tick_marks, sorted_label_list, rotation=45)
plt.yticks(tick_marks, sorted_label_list)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')

# Construct normalized confusion matrix plot
plt.figure(2)
plt.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Greens)
plt.title("Normalized Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(NUM_GENRES)
plt.xticks(tick_marks, sorted_label_list, rotation=45)
plt.yticks(tick_marks, sorted_label_list)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')

# Output plots
plt.show()
