import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Main {

	public static void main(String[] args) 
	{
		try 
		{
			// Read every file in the directory and turn it into the object of class Text
			String[] genres = {"Adventure", "Fantasy", "Horror", "Romance", 
					"SciFi", "Western", "CrimeMystery", "FairyTale"}; // list of the genre folders
			
			for(String genre : genres)
			{
				File directory = new File("genres\\" + genre);
				File[] directoryListing = directory.listFiles(); // list of files in the directory

				// if the directory isn't empty
				if (directoryListing != null) 
				{
					//for each file create an object of the class Text
					for (File file : directoryListing) 
					{
						Text text = new Text(file.getPath());
						String fileName = text.getFileID(); // name of the file
						List<String> txt = text.getTokens(); // tokenized text
						
						// Write the tokenized versions to the files with the same name
						
						// create the printwriter object
						PrintWriter writer = new PrintWriter(("genres\\" + genre + "\\" + fileName + ".txt"), "UTF-8");
					    
					    System.out.println("writing the file: " + fileName);
					    
					    // write the tokenized texts to the files
					    for(String sent : txt)
					    {
					    	writer.println(sent);
					    }
					    writer.close();
					}
				}
			}
		}
		catch (IOException e) 
		{
			e.printStackTrace();
		}
	}
}
