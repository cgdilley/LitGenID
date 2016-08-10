
# Gutenberg Module

This document will detail the various contents of the Gutenberg module, which was responsible for filtering and labeling the complete collection of texts from [Project Gutenberg][3].

[TOC]

## **Directories**

These directories, other than the *src* directory, are not included in the Git repository because of their enormous sizes. 

### Data

The data directory contains the texts downloaded by the Project Gutenberg's robot tool ([link][1]).  We used this tool to collect all available English-language texts in plain-text (.txt) format.  Most of the texts are UTF-8/ASCII encoded, but some are ISO-8859-1 encoded as well.  All texts contained within are labelled with their Gutenberg eBook ID# as their file name.  Each file is contained within its own individual directory that also has this same eBook ID#.  These directories are also nested in a directory structure that allows one to search for a file with a particular ID number digit by digit, so that not all files are piled in one single directory.

These text files also contain meta information and legal information relating to the text.  The meta information indicating the books' titles and authors needed to extracting from this, and all of the non-book text needed to be trimmed before placing in the corpus.

There seems to be no obvious structure to how ID numbers are assigned to the various texts, and there are several duplicate books within the collection that needed to be identified and removed.

### ePub

The epub directory contains catalog information relating to the Gutenberg texts, acquired from the Project Gutenberg website ([link][2]).  This directory, unlike the data directory, does not have any structure designed to distribute its contents at all, and contains individual directories labelled with every Gutenberg eBook ID#.  These sub-directories contain .rdf files with information about their corresponding text, described with an XML structure.

### Corpus

The CORPUS directory contains the output from all processing undertaken by the Gutenberg module.  This directory contains sub-directories labelled for each genre that is to be identified in this machine learning project.  Each of these sub-directories contain all text files that were able to be labelled with the corresponding genre label, copied from the data directory with the unnecessary information trimmed out.

The CORPUS directory also contains a file *"catalog.csv"* that is a file in CSV format containing information relating to all texts in the corpus, including each book's title, its author(s), its labelled genres, and paths to all places in the corpus where it is located.  The python script *"catalogManager.py"* in this directory serves to help navigate this catalog, allowing one to query for any of these criteria easily.

### Src

The src directory contains all source Python files, described in greater detail below.

## **Sources**

The code responsible for every stage of processing was written in separate python scripts, each of which are treated as being executed from the root *Gutenberg* directory (rather than from the *src* directory in which they are located).

### Extract.py

This script is responsible for the first stage of the processing sequence, which involved going through all text files in the *data* folder, and identifying the title and author of the text.  This title and author information, along with the path to the file, is then stored and eventually written to the file *"textData.txt"* in CSV format.

Titles are identified by lines that began with the string *"Title:"*.  The remaining contents are determined to be the title of the book, and any leading or trailing whitespace is trimmed.

Authors are identified by lines that began with the string *"Author"*.  However, the process of converting the remaining contents of the line into a list of authors is more complicated.  A number of aspects of the string are altered (such as removing certain symbols, or text inside parentheses) in order to more accurately pick out the authors' names.  The string is also split by the word "and" and by commas, and each split component is treated as its own author in the list of authors.  This process does a decent job of properly attributing a particular author when that author has their name written differently in different texts or when they are a single author in a group of authors.

Not all texts in the collection have effectively-labelled title and author information.  Any texts where this information is unable to ascertained are discarded.  This amounted to roughly 1% of the total texts in the collection.  Also, many texts had two text files for a single eBook ID# that were identical other than in their text encoding.  In such cases, just the UTF-8 encoded text was considered, and the other ignored.  This process narrowed down the 69199 text files in the collection down to 41430.

The python script **extract_utils.py** contains some functions used by extract.py, separated out for a cleaner appearance.

### FindLabels_Guten.py

This script is responsible for reading the data output by **extract.py**, and using the Gutenberg catalog files in the *epub* directory to attribute a genre to the files.

For this, the script first loads the title, author, and file path information stored in *textData.txt*.  The eBook ID# of the book is implied by the file path, and is used to look up the book in the catalog.  The catalog files are in XML format, and contain any number of "bookshelf" elements, which are akin to genres in the Project Gutenberg system.  These bookshelves are identified in the XML tree, and if they match the set of accepted genres, the book's information along with this label are stored and later written into *"textDataWithGenre.txt"* in CSV format.

This process reduced the 41430 texts from **extract.py** down to 1750 labelled texts.  Many of the texts on Project Gutenberg are poems, short stories, plays, historical documents, and other non-novel texts that are not the focus of our research, and so this level of reduction is not surprising.

### FindURLs_IBList.py

This script is responsible for finding title and author matches of book data output by **extract.py** on the Internet Book List ([link][4]), and storing links to the book's information page on this website.

This is accomplished by formatting the title and author of the book into a search query URL for the website, requesting the page at the URL, and parsing the HTML response.  This response contains a well-formatted list of titles and authors, with links to information pages relating to the titles and authors referenced.  Matches are determined by employing weak/fuzzy string comparisons, to account for variations in how titles and authors were written.

If a match is found, the URL linking to the book's information is stored along with the other book information, and eventually written to *"textDataWithURL.txt"*.  This process takes a very long time (~10 hours) to run for all 41430 texts, and so results are written progressively and the already-searched texts are marked so that the process can be stopped and started without having to start over in case something happens.

This process reduced the 41430 texts from **extract.py** down to 1245 texts with associated URLs.  It is unclear if this is an expected amount, or if many texts were lost due to not being properly matched when they should have.

### FindLabels_IBList.py

This script is responsible for using the URLs output by **findURLs_IBList.py** to query for the book information located at the URLs and assign a genre to the associated book.

This is accomplished by extracting the title, author, file path, and URL information stored in *"textDataWithURL.txt"*, and requesting the page located at the URL.  The HTML response is then parsed to determine whether the book is categorized as a novel (if not, it is discarded), and any genres associated with the book are extracted.  Any genres found that match the list of acceptable genres are attributed to the books, stored, and eventually written to *"textDataWithGenre2.txt"*.

This process reduced the 1245 texts from **findURLs_IBList.py** down to 458 labelled texts.

### FindLabels_utils.py

This script contains a lot of utility methods used by **findLabels_Guten.py**, **findURLs_IBList.py**, and **findLabels_IBList.py**, as well as the class *TextData*.  This class is used to easily store information about individual books and accessing particular data stored in fields, such as title, author, etc.

### ProcessResults.py

This script is responsible for merging the outputs of **findLabels_Guten.py** and **findLabels_IBList.py**, as well as merging/removing any duplicates, and converting their identified genres into a consistent schema of accepted genres.  This script also produces a nice human-readable summary of the entire collection of labelled texts.

This is accomplished by first loading in the contents of both *"textDataWithGenre.txt*" and *"textDataWithGenre2.txt"*.  These elements are added one by one, checking that the referenced file path for each is unique (so that the same file is not referred to twice and thus duplicated).  To account for the fact that the Gutenberg files also have multiple text files and ID numbers containing the same book, titles are also tested for uniqueness when merging.  If a title match is found, it also tests that there is an author match as well (with fuzzy string matching), so that two books with the same title by different authors are still considered separate.  

If duplicates are found, whichever was added first takes precedence and any further matches are discarded.  Before being discarded, however, their sets of labels/genres are merged in case the to-be-discarded text carries a label not yet assigned to the retained text.

As the genres assigned by Gutenberg and by IBList aren't identical, and don't fall into the same buckets we wish to use for this research, all assigned genres are also mapped to an official set of genres used for labeling.

The merged, labelled list of books is eventually written to *"textData_FINAL.txt"*.

This process merged the 1750 texts from **findLabels_Guten.py** and the 458 texts from **findLabels_IBList.py** into one collection of 1964 labelled texts.

The python script **processResults_utils.py** contains some functions used by processResults.py, separated out for a cleaner appearance.

### AssembleCorpus.py

This script is responsible for reading the final labelled set of book information, constructing the corpus directory structure, and copying the files from the Gutenberg data into the corpus folders after trimming excess textual content from them.  A catalog of this corpus is also generated.

This is accomplished by reading the *"textData_FINAL.txt*" file, getting the title, author, file path, and genre information for all books to be in the final corpus.  The corpus structure (with the genre sub-directories) is then generated, if it does not already exist.  Then, all texts are iterated through, reading the text contents of each file at the associated file path.  The beginning and end of the actual text component are determined, and this content is written to a new file (identified by its Gutenberg eBook ID#) in each of the folders corresponding to its associated genres.

This means that the same text will occur in two different genre sub-directories if it has multiple genres attributed to it.  Only about 5% of all texts had multiple genres.  

The extracted book information is then written into *"CORPUS/catalog.csv"*, with the original Gutenberg file path replaced with a list of paths to all of the text's occurrences within the corpus.

## **Text Files**

The text files are mostly used as intermediary output between the different processing components.

 - **textData.txt** - Output from *extract.py*, input for *findLabels_Guten.py* and *findURLs_IBList.py*.
 - **textDataWithURL.txt** - Output from *findURLs_IBList.py", input for *findLabels_IBList.py*.
 - **textDataWithGenre.txt** - Output from *findLabels_Guten.py*, input for *processResults.py*.
 - **textDataWithGenre2.txt** - Output from *findLabels_IBList.py*, input for *processResults.py*.
 - **textData_FINAL.txt** - Output from *processResults.py*, input for *assembleCorpus.py*.
 - **saveMarker.txt** - File for persistently holding how far progressed *findURLs_IBList.py* is. 
 - **genreCounts.txt** - Pretty, human-readable output from *processResults.py*, detailing the texts that make up the corpus and the genres to which they belong.






[1]: http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages
[2]: http://www.gutenberg.org/wiki/Gutenberg:Feeds
[3]: http://www.gutenberg.org/
[4]: http://www.iblist.com/
> Written with [StackEdit](https://stackedit.io/).