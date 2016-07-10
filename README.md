# Outline for ML project

## Premise

We intend to apply machine learning methodology to determine the genre of a particular text based on its textual content.

What kind of genres remains to be determined.  Do we want to differentiate texts based on very broad categories such as "Fiction" and "Non-fiction", "Poetry", or whatever else?  Or do we want to get more specific, such as "Romance" or "Mystery"?  If the latter, do we want to limit ourselves to just fiction novels?

## Data Source

We plan to use freely available books from [Project Gutenberg](https://www.gutenberg.org/).  Other sources of freely available data may be considered (such as the [Corpus of Contemporary American English](http://corpus.byu.edu/coca/)).  We also may ask Coltekin what other sources we may have access to through the university.

We must determine what kind of texts we want to include in our dataset.  If we are looking to differentiate more specific genres, we may wish to limit our dataset to fiction novels, for example.

Texts can be downloaded as described on [this](http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) page.  Downloading the texts will likely take a very long time, as there are quite a lot.  Maybe something to let run overnight.  Until we determine how we wish to filter our dataset, however, this is not immediately necessary.


## Processing of Data

If we choose to utilize the unstructured data from Project Gutenberg, then we will have to do pre-processing of the text ourselves.  This would include extracting any meta-data and would likely involve splitting sentences and tokenizing the text.

Briefly looking at the few texts I've already downloaded, it seems that it will also take some effort disentangling the files and extracting useful information.  It also seems that they are **not** labelled with any kind of genre information, so we may need to attach such labels ourselves from some other source.  Somewhere may exist a database that attributes a genre to a particular book that we can utilize for labeling our training set.

Parsing of the texts may be considered, but only if everything else is going smoothly.

## Programming Language and Tools

We must decide upon which programming language we would like to work in primarily.  Some small tools for pre-processing and whatnot can be built in any arbitrary language, but the bulk of the code should be in one language that we are all comfortable working with.  For me, Java is my most comfortable language (or other C-derivatives), but I wouldn't mind working in Python if that is preferred by others.

After determining our language of choice, we will have to find which machine learning tools we wish to use along with it.  For Python we can use the tools we've already been using in the course.  For Java, we can use the same sort of libraries that we are utilizing in the SNLP course (specifically, [WEKA](http://www.cs.waikato.ac.nz/ml/index.html)).  Any other options that we may be familiar with are possibilities as well.

## Learning from the Data

The most critical aspect of the project is determining what machine learning tools we intend to employ.

We could simply apply clustering of the data based on some measurable aspects of the texts.  This would alleviate the need to have labelled data, but I think it would be difficult to get good clusters and be able to derive anything meaningful from them.

We could utilize standard feed-forward neural networks, or perhaps an RNN variant if we were ambitious.  This is probably the most straightforward solution in general.

The solution that appeals most to me, however, is the usage of a CNN.  This makes sense to me, as determining what is or isn't of a certain genre is difficult to define in concrete terms, so leaving the computer to figure it out based on labelled data seems best.  CNNs would allow us to simply run convolutions over the text and determine what combinations of features suggest a particular genre without any real strong direction from us.  

Useful description of CNNs (for images):  [link](https://www.youtube.com/watch?v=py5byOOHZM8)
Useful visualization of the CNN process (for images):  [link](https://www.youtube.com/watch?v=BFdMrDOx_CM)

The above videos are quite excellent for explaining the idea behind CNNs.  They apply to images specifically, for which there are a lot of obvious convolutions (blurring, edge detection in various directions, etc).  However, convolutions for NLP are not quite as obvious.  Perhaps we can get some direction from Coltekin about what kind of convolutions to apply, if we decide to go this route.

## Summary of Tasks

#### First Steps

 - Determine what exactly we're hoping to identify in terms of genres
 - Determine where to assemble our data from
 - Determine what kind of filtering we wish to apply to that data
 - Determine machine learning methodology to employ
 - Decide upon programming language of choice and tools to utilize that best suit our needs

#### Other Steps

 - Pre-process the data into a useful form
 - If applicable, assign labels to data for any supervised learning methods
 - Construct and implement our machine learning model, tweaking as we see fit until reaching a satisfactory conclusion.






> Written with [StackEdit](https://stackedit.io/).