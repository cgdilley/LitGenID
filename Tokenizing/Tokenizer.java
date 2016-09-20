import java.util.List;
import java.util.ArrayList;
import java.io.InputStream;
import java.io.IOException;

import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;


/**
 * This class tokenizes a text given, using the Sentence Detector and the Tokenizer 
 * from the OpenNLP toolkit.
 * There's only one property available publicly - the tokenized version of the given text.
 * @author Inna Pirina
 */
public class Tokenizer {
 
 private SentenceModel sentModel;
 private SentenceDetectorME sentDetectorME;
 
 private TokenizerModel tokenizerModel;
 private TokenizerME tokenizerME;
 
 private List<String> sentTokens;
 
 /**
  * Constructor for the class
  * @param text - a string to be tokenized
  * all the OpenNLP tools are initialized.
  */
 public Tokenizer(String text) 
 {
	 sentModel = makeSentModel();
	 sentDetectorME = makeSentDetector();
	 tokenizerModel = makeTokenizerModel();
	 tokenizerME = makeTokenizer();
	 sentTokens = tokenize(text);
 }
 
 
 /**
  * Initializes the Sentence Model, using the file provided by OpenNLP.
  * The model will be used later to detect sentences.
  * @return sentModel 
  */
 private SentenceModel makeSentModel() 
 {
	 InputStream stream = this.getClass().getResourceAsStream("en-sent.bin");
	 try 
	 {
		 sentModel = new SentenceModel(stream);
	 }
	 catch (IOException e) 
	 {
		 e.printStackTrace();
	 }
	 finally {
		 if (stream != null) 
		 {
			 try 
			 {
				 stream.close();
			 }
			 catch (IOException e) 
			 {
				 e.printStackTrace();
			 }
		 }
	 }
	 return sentModel;
 }
 
 
 /**
  * Given the already initialized model, creates a sentence detector.
  * @return sentDetectorME
  */
 private SentenceDetectorME makeSentDetector() 
 {
  sentDetectorME = new SentenceDetectorME(sentModel);
  return sentDetectorME;
 }
 
 
 /**
  * Initialized the tokenizer model, using the file provided by OpenNLP tools.
  * Will later be used to split sentences into tokens
  * @return tokenizerModel
  */
 private TokenizerModel makeTokenizerModel() 
 {
	 InputStream stream = this.getClass().getResourceAsStream("en-token.bin");
	 try 
	 {
		 tokenizerModel = new TokenizerModel(stream);
	 }
	 catch (IOException e) 
	 {
		 e.printStackTrace();
	 }
	 finally 
	 {
		 if (stream != null) 
		 {
			 try 
			 {
				 stream.close();
			 }
			 catch (IOException e) 
			 {
				 e.printStackTrace();
			 }
		 }
	 }
	 return tokenizerModel;
 }
 
 
 /**
  * Given the already existing tokenizer model, initializes the tokenizer.
  * @return tokenizerME
  */
 private TokenizerME makeTokenizer() 
 {
  tokenizerME = new TokenizerME(tokenizerModel);
  return tokenizerME;
 }
 
 
 /**
  * Given the initialized OpenNLP models, the method splits the given string into
  * tokens, which are put in a list. 
  * Because of the OpenNLP functionality, the string is first split into sentences 
  * and then each sentence is split into tokens. 
  * @param text - the string representation of a text to be tokenized.
  * @return tokens - ArrayList of tokens of the text.
  */
 private List<String> tokenize(String text) 
 {
	 sentTokens = new ArrayList<String>(); // the list of tokens
	 String[] sentences;
	 String[] sentenceTokens;
	 
	 // split the text into sentences 
	 sentences = sentDetectorME.sentDetect(text);
  
	 // for each sentence, split the sentence into tokens and add the tokens to the list
	 for(int i = 0; i < sentences.length; i++) 
	 {
		 sentenceTokens = tokenizerME.tokenize(sentences[i]);
		 String sent = sentenceTokens[0] + " ";
		 for(int j = 1; j < sentenceTokens.length; j++) 
		 {
			 sent += sentenceTokens[j] + " ";
		 }
		 sentTokens.add(sent);
	 }
  return sentTokens;
 }
 
 // the get method for tokens
 public List<String> getTokens()
 {
	 return sentTokens;
 }

}




