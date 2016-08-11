# Outline for ML project

## Premise

We intend to apply machine learning methodology to determine the genre of a particular novel based on its textual content.

The genres we wish to identify are as follows:

 - Adventure
 - Crime/Mystery
 - Fairy tale
 - Fantasy
 - Horror
 - Romance
 - Science Fiction
 - Western

## Data Source

We are utilizing texts acquired from [Project Gutenberg](http://www.gutenberg.org) as well as [ManyBooks](http://manybooks.net/).

#### **Project Gutenberg**

After downloading all texts made available from their [download](http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) page, we extracted as much information from the raw text files as possible and used various methods to assign genre labels to these texts.  An explanation of this entire process can be found in *Gutenberg.md*, and all files associated with the process are found in the *Gutenberg/* directory.

By doing so, we managed to collect and successfully label 1964 texts.

#### **ManyBooks**

???


## Processing of Data

After acquiring all texts and sorting them by genre, we will need to process the files to prepare them for the machine learning process.  This will likely entail cleaning out useless data from the files, and then tokenizing them.  

We will have to determine and decide upon the most effective means of tokenizing the data, and apply it consistently across all texts in our corpus.

## Programming Language and Tools

We are primarily working with Python, but each portion of the project is independent enough to not strictly require it.  We will likely be using [Keras](https://keras.io/) as our machine learning tool of choice.

## Learning from the Data

The most critical aspect of the project is determining what machine learning tools we intend to employ.

We could simply apply clustering of the data based on some measurable aspects of the texts.  This would alleviate the need to have labelled data, but I think it would be difficult to get good clusters and be able to derive anything meaningful from them.

We could utilize standard feed-forward neural networks, or perhaps an RNN variant if we were ambitious.  This is probably the most straightforward solution in general.

The solution that appeals most to me, however, is the usage of a CNN.  This makes sense to me, as determining what is or isn't of a certain genre is difficult to define in concrete terms, so leaving the computer to figure it out based on labelled data seems best.  CNNs would allow us to simply run convolutions over the text and determine what combinations of features suggest a particular genre without any real strong direction from us.  

Useful description of CNNs (for images):  [link](https://www.youtube.com/watch?v=py5byOOHZM8)
Useful visualization of the CNN process (for images):  [link](https://www.youtube.com/watch?v=BFdMrDOx_CM)

The above videos are quite excellent for explaining the idea behind CNNs.  They apply to images specifically, for which there are a lot of obvious convolutions (blurring, edge detection in various directions, etc).  However, convolutions for NLP are not quite as obvious.  Perhaps we can get some direction from Coltekin about what kind of convolutions to apply, if we decide to go this route.

## Summary of Tasks

#### Completed tasks

 - Determine what exactly we're hoping to identify in terms of genres
 - Determine where to assemble our data from
 - Determine what kind of filtering we wish to apply to that data
 - Decide upon programming language of choice and tools to utilize that best suit our needs
 - Download text data and assign genre labels to them

#### Next steps

 - Merge disparate corpora from our multiple sources into a single, consistent corpus
 - Pre-process the data into a useful form
 - Determine machine learning methodology to employ

#### Other steps

 - Construct and implement our machine learning model, tweaking as we see fit until reaching a satisfactory conclusion.






> Written with [StackEdit](https://stackedit.io/).