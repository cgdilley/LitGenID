import os
from keras.preprocessing.text import Tokenizer

# Path to corpus files
TEXT_DATA_DIR = "./Corpus/RAW/"

results = []
types = set()

for name in sorted(os.listdir(TEXT_DATA_DIR)):
    path = os.path.join(TEXT_DATA_DIR, name)
    if os.path.isdir(path):
        genreFiles = sorted(os.listdir(path))

        print("\nCounting genre %s...\n------------------" % name)

        texts = []
        # Iterate through all files in the labelled folder
        for findex in range(len(genreFiles)):
            fname = genreFiles[findex]

            # If we're looking at a text file, load it
            if ".txt" in fname:
                fpath = os.path.join(path, fname)
                # Open the file
                f = open(fpath)
                texts.append(f.read())
                # Close the file
                f.close()

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(texts)
        word_count = tokenizer.word_counts

        types |= set(word_count.keys())

        fileCount = len(texts)
        tokenCount = sum(word_count.values())
        typeCount = len(word_count)
        results.append(dict({"files": fileCount,
                             "tokens": tokenCount,
                             "types": typeCount}))
        print("Files:  %d" % fileCount)
        print("Tokens: %d" % tokenCount)
        print("Types:  %d" % typeCount)

print("\nTOTALS:\n=======================")
print("Files:  %d" % sum([x["files"] for x in results]))
print("Tokens: %d" % sum([x["tokens"] for x in results]))
print("Types:  %d" % len(types))


