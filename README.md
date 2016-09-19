# Outline for ML project

## Premise

The purpose of this project is to train a machine learning model to ascertain the literary genre of a novel based on its textual content.  This is something humans can do intuitively (with some subjectivity), but would be challenging to explicitly define and identify by direct means in a computer program.  We are hoping that the model will be able to pick up on the qualities of a book that cause it to belong to a particular genre, and have some success at labeling unknown texts.  To narrow the scope of the identification, we are limiting the model to identify **fiction novels** that belong to one (or more) of the following genres:

 - Adventure
 - Crime/Mystery
 - Fairy Tale
 - Fantasy
 - Horror
 - Romance
 - Science Fiction
 - Western

## Data Source

We are primarily utilizing texts acquired from [ManyBooks](http://manybooks.net/).  We also used some texts downloaded directly from [Project Gutenberg](http://www.gutenberg.org) to fill in some gaps, but the bulk of the data came from ManyBooks.  The process by which we acquired these texts is detailed below.

#### **ManyBooks**

???

#### **Project Gutenberg**

After downloading all texts made available from their [download](http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) page, we extracted as much information from the raw text files as possible and used various methods to assign genre labels to these texts.  An explanation of this entire process can be found in *Gutenberg.md*, and all files associated with the process are found in the *Gutenberg/* directory.

By doing so, we managed to collect and successfully label 1964 texts.

However, we found that most of these texts acquired and labelled in this manner made up a smaller subset of the ManyBooks data set.  As a result, only a small handful of these texts were utilized in the final corpus (specifically, those texts belonging to the Crime/Mystery and Fairy Tale genres).  


## Processing of Data

After acquiring all texts and sorting them by genre, we underwent a process of preprocessing the data.  This involved cleaning up unnecessary garbage from the texts, as well as conforming them all to a standardized tokenization scheme.    

### Description of tokenization process

?????

## Final Corpus Results

After preprocessing, we were left with our final corpus of labelled texts.  In total, the corpus contains XXXX individual texts with XXXXX individual tokens with XXXX token types.  These texts are divided into separate folders representing the 8 genres they were labelled by.  Some of the texts are duplicates, as texts that belonged to multiple genres were copied and placed in the folders of all applicable genres.

A breakdown of the corpus by genre is depicted below:

<<<<<<<< INSERT SOME KIND OF TABLE HERE >>>>>>>>>>>>>>>>

## Implementing the Machine Learning

We attempted a couple of different approaches for defining models to train on our corpus.  

Firstly, we chose to employ a convolutional neural network model.  Texts had their most frequent words removed, and were trimmed or padded to a consistent length.  All words were then represented as word vectors as defined by [GloVe](http://nlp.stanford.edu/projects/glove/) before being fed into the model.

Secondly, we utilized a recurrent neural network model as well.
????????????

### Convolutional neural network model

We opted to write our CNN model utilizing much of the code used in Assignment #3, tweaked to suit this purpose and overall improved.  This code was written in Python, using the the [Keras](www.keras.io) library.  All code related to this process is included in the *"Learning/"* directory.

The first stage of the process involved simplifying the text data from string tokens into integers, and creating a word index linking words to these integers.  The total frequency of all tokens was calculated as part of this process as well.  We accomplished this using Keras's tokenizer.  

Due the large size of the corpus data, it became difficult to process the entirety of the texts in this manner due to memory constraints.  As such, we opted to pare the texts down further by removing the 1200 most frequent tokens.  This eliminated approximately 78% of the tokens in the documents.  This value was arbitrarily chosen after manually looking through the ranked list of words and after consulting the graph depicted below.  We feel this would have little impact on the learning capabilities of the model, as most of these words would not hold much predictive power.  However, due to limited time, we were unable to tweak this number much in either direction to observe the resulting differences.  As a result, this assertion is purely conjecture.

<<<<<< INSERT RANK VOLUME GRAPH >>>>>>>>>>>>>>

Furthermore, we limited all texts to contain no more than 12000 tokens after removing the most frequent tokens.  Texts that contained fewer than this many were padded with 0-tokens to reach this 12000 value.  In the end, all texts contained exactly 12000 integer values representing specific words.  The word index that linked words to their integer representation was also saved into a CSV file.

After performing this processing, all texts were saved in a separate folder in this format in order to prevent having to repeat this time-consuming task.  All code related to this process can be found in "*Learning/embed.py*"

The second stage of this process involved loading these processed texts, and feeding them into the CNN model.  This was done by forming the texts into a multi-dimensional array of integer values as well as a vector of label values.  Word embedding vectors from GloVe were also loaded, and the words represented by the texts' integers were mapped to their corresponding word vectors.  After experimenting with the 50-, 100-, and 200-dimensional vectors from GloVe, it was found that the 50-dimensional vectors had the best results (in additional to being processed quicker).

The architecture of the model contains the following layers, in sequence:

 - An embedding layer which converts the word identifiers into their corresponding word vectors
 - A convolutional layer, with **16** convolutional kernels and a filter depth of **32**.
 - A max-pooling layer, pooling by a factor of **8**.
 - A flattening layer, converting the 2-dimensional output from the previous layers to one dimension.
 - A densely-connected layer, with **128** outputs.
 - A densely-connected layer, with as many outputs as genres (**8**, generally).

These values were settled upon after trying a number of different configurations and tracking their results.  Increasing any of these numbers tended to give worse results, presumably suffering from overfitting issues.

After performing 10-fold cross-validation, with 2 training epochs per fold, we obtained the following results:

<<<<<<<<<<<<<<<<<<< INSERT RESULTS >>>>>>>>>>>>

It is clear from these results that the imbalance in the number of texts per genre has played a significant role.  The model predominantly attempts to classify the texts as either *Adventure*, *Romance*, or *SciFi*, as these are most highly populated genres.  The other genres as predicted by the model far less often, certainly much less than expected based on their relative proportions.

To try combat this issue, we tried utilizing the same model, but limiting each genre to no more than 400 texts each.  In the interests of time, this was performed on only one fold for one training epoch.  The results were as follows:

<<<<<<<<<<<<<<<<<<<<< INSERT RESULTS >>>>>>>>>>>

Making this change greatly reduced the accuracy of the model, but did improve its precision and recall.  However, this is overall a worse result.

Out of curiosity, we ran the model using only those three most frequent genres in order to observe how well the model differentiates between them when alone.  As with the previous experiment, this was performed on only one fold for one training epoch.  These were the results:

<<<<<<<<<<<<<<<<<<<<< INSERT RESULTS >>>>>>>>>>>

These results show improved accuracy and greatly improved precision and recall, and shows the model's overall power in differentiating genres given sufficient training data.  However, this level of accuracy is still not terribly reliable, and would likely not be good enough for a real-world classification system.

Some improvements may have been found by tweaking the processing to include more (or less) of the tokens found in the texts, as well potentially by combining the results of several models into one larger model.  If given time and reason to expand on this system, these are the most likely paths for optimization we would follow.  

### Recurrent neural network model

???????????????


## Conclusion

 ???????????????????????????????






> Written with [StackEdit](https://stackedit.io/).