import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.commons.io.FileUtils;

/**
 * @author Inna Pirina
 * The core information to store for each text:
 * – File id
 * – Text content
 * - tokens - tokenized text
 */
public class Text {
	
	private String content;
	private String fileID;
	private List<String> tokens;
	
	/**
	 * Default constructor for the class
	 */
	public Text()
	{
		fileID = ""; 
		content = ""; 
		tokens = null;
	}
	
	/**
	 * Constructor method that takes path to a file as a parameter
	 * @param filePath
	 * @throws IOException
	 */
	public Text(String filePath) throws IOException
	{
		fileID = extractFileID(filePath);
		content = readText(filePath);
		tokens = new Tokenizer(content).getTokens();
		
	}

	
	/**
	 * reads the content of the file
	 * @param filename - the name of the file
	 * @return 
	 * @throws IOException
	 */
	private String readText(String filePath)
	{
		String text = "";
		try 
		{
			text = FileUtils.readFileToString(new File(filePath), "UTF-8");
		} 
		catch (IOException e) {
		    System.err.println("Caught IOException: " + e.getMessage() + "");
		}
		return text;
	}
	
	/**
	 * takes the path of the file and extracts the name only
	 * @param filePath
	 * @return name of the file
	 */
	private String extractFileID(String filePath) 
	{
		File f = new File(filePath);
		String id = f.getName();
		return id.substring(0, (id.length()-4));
	}
	
	
	// All the get methods:
	
	public String getFileID()
	{
		return fileID;
	}
	
	public String getContent()
	{
		return content;
	}
	
	public List<String> getTokens()
	{
		return tokens;
	}

}
