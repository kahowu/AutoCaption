package aligner;

import edu.cmu.sphinx.frontend.util.AudioFileDataSource;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;
import edu.cmu.sphinx.linguist.language.grammar.TextAlignerGrammar;

import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;
import java.net.URL;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * A simple example that shows how to align speech to existing transcription to
 * get times.
 */
public class Aligner {
	private static String readFile(String path) {
    // Location of file to read
	    File file = new File(path);
	
	    try {	
            Scanner scanner = new Scanner(file);
            String str = "";//the final string

            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                str = str + line + " ";
            }
            scanner.close();
            System.out.println(str);
            return str;
	    } catch (FileNotFoundException e) {
	        e.printStackTrace();
	    }
	    return null;
	}

    public static void main(String[] args) throws IOException, UnsupportedAudioFileException {

        ConfigurationManager cm = new ConfigurationManager("src/config/aligner.xml");
        Recognizer recognizer = (Recognizer) cm.lookup("recognizer");

        TextAlignerGrammar grammar = (TextAlignerGrammar) cm.lookup("textAlignGrammar");
//        String input_url = "input/"+ args[0];
//        String content = readFile(input_url); 
//        grammar.setText(content);
        grammar.setText("testing testing testing this is a test");
        
        recognizer.addResultListener(grammar);
        
        /* allocate the resource necessary for the recognizer */
        recognizer.allocate();

        // configure the audio input for the recognizer
        AudioFileDataSource dataSource = (AudioFileDataSource) cm.lookup("audioFileDataSource");
        dataSource.setAudioFile(new URL("file:audio/test.wav"), null);
//        String audio_url = "file:audio/" + args[1]; 
//        dataSource.setAudioFile(new URL(audio_url), null);

        Result result;
        while ((result = recognizer.recognize()) != null) {

            String resultText = result.getTimedBestResult(false, true);
            System.out.println(resultText);
        }
    }
}
