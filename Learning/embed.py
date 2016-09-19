from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
import os
import gc
import errno
import progressbar
import time
import csv
import numpy as np
np.random.seed(1337)

"""
EMBED.PY
This script is designed to take the raw (tokenized) input files, and convert them into series of integers rather than
strings to allow for more efficient processing.  Also creates an index file for all words and labels found in this
process.

"""

# Directory in which the raw corpus (input) files are located
TEXT_DATA_DIR = "./Corpus/RAW/"
# Directory to which the processed (output) files are to be placed
TEXT_DATA_OUTPUT_DIR = "./Corpus/PROCESSED/"
# Path to the word index file to be created
WORD_INDEX_FILE = "./Corpus/PROCESSED/index.txt"
# Path to the label index file to be created
LABEL_INDEX_FILE = "./Corpus/PROCESSED/labels.txt"
# Rank threshold that words must surpass to be included (more frequent words are discarded)
RANK_THRESHOLD = 1200
# Max threshold that words must be under to be included (less frequent words are discarded)
MAX_NB_WORDS = 50000
# Number of tokens in all documents after processing (longer documents will be cropped, shorter will be padded)
MAX_SEQUENCE_LENGTH = 12000

# The input text files
texts = []
# A running dictionary of labels found
labels_index = {}
# Labels of the input text files
labels = []
# Filenames of the input text files
filenames = []

print("LOADING TEXTS...\n------------------------------------")

# Iterate through all files in the input directory
for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)

    # If a folder is found, assume it is a label
    if os.path.isdir(path):

        # Add label to the labels index
        label_id = len(labels_index)
        labels_index[name] = label_id

        # Get list of all files in this folder
        genreFiles = sorted(os.listdir(path))

        print("Loading genre %s:" % name)
        time.sleep(0.005)  # So that this print statement doesn't mess with the progress bar

        bar = progressbar.ProgressBar(max_value=len(genreFiles))
        # Iterate through all documents in the folder
        for findex in range(len(genreFiles)):
            fname = genreFiles[findex]

            bar.update(findex)

            # If a text file is found, read it and add it to the text, label, and filename lists
            if ".txt" in fname:
                fpath = os.path.join(path, fname)
                filenames.append(fname)
                f = open(fpath)
                texts.append(f.read())
                f.close()
                labels.append(label_id)
        bar.finish()

time.sleep(0.005)
print("\nTOKENIZING TEXTS...\n-------------------------------")

# Construct the tokenizer and fit it on all processed texts.  This is the bulk of the work done by this program.
tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Free up memory
del texts
gc.collect()
time.sleep(1)

# Remove the most common words from the sequences
# (The integer that is assigned to represent each word is its rank, so it is a simple matter to
#  determine which words should be cut without consulting the word index)
for i in range(len(sequences)):
    sequences[i] = [x for x in sequences[i] if x >= RANK_THRESHOLD]

# Get the word index and the word counts, and get the total token count
word_index = tokenizer.word_index
word_counts = tokenizer.word_counts
total_tokens = sum(word_counts.values())
print('Found %s unique tokens.' % len(word_index))
print('Found %s total tokens.' % total_tokens)

# Pad the sequences to the suggested length, or if not set, to the maximum length required by the documents
print("Padding sequences...")
if MAX_SEQUENCE_LENGTH > 0:
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
else:
    data = pad_sequences(sequences)

# Free up more memory
del sequences
gc.collect()

print("\nWRITING TOKENIZED TEXTS TO FILE...\n------------------------------")

bar = progressbar.ProgressBar(max_value=len(data))
for i in range(len(data)):
    bar.update(i)

    # Make the label directory, if it doesn't already exist
    lpath = os.path.join(TEXT_DATA_OUTPUT_DIR, str(labels[i]))
    try:
        os.makedirs(lpath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Build the output file path by joining the directory with the file's name
    fpath = os.path.join(lpath, filenames[i])

    f = open(fpath, "w")

    # Merge the contents of the data list into a single string, and output to file
    f.write(" ".join(map(str, data[i])))

    f.close()
bar.finish()

time.sleep(0.005)
print("Writing index files...")

# Create the word index CSV file (includes word counts)
with open(WORD_INDEX_FILE, "w") as f:
    csv_out = csv.writer(f)

    csv_out.writerow(["WORD", "INDEX", "COUNT"])

    for word, index in sorted(word_index.items(), key=lambda i: i[1]):
        csv_out.writerow([word, index, word_counts[word]])

# Create the label index CSV file
with open(LABEL_INDEX_FILE, "w") as f:
    csv_out = csv.writer(f)

    csv_out.writerow(["LABEL", "INDEX"])

    for label, index in labels_index.items():
        csv_out.writerow([label, index])


labels = to_categorical(np.asarray(labels))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)







