/*
 * @Author: Jeff Wu and David Lu
 */
package edu.cmu.sphinx.demo.aligner;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import edu.cmu.sphinx.alignment.LongTextAligner;
import edu.cmu.sphinx.api.SpeechAligner;
import edu.cmu.sphinx.result.WordResult;

/**
 * This class demonstrates how to align audio to existing transcription and
 * receive word timestamps.
 *
 * <br/>
 * In order to initialize the aligner you need to specify several data files
 * which might be available on the CMUSphinx website. There should be an
 * acoustic model for your language, a dictionary, an optional G2P model to
 * convert word strings to pronunciation. <br/>
 * Currently the audio must have specific format (16khz, 16bit, mono), but in
 * the future other formats will be supported. <br/>
 * Text should be a clean text in lower case. It should be cleaned from
 * punctuation marks, numbers and other non-speakable things. In the future
 * automatic cleanup will be supported.
 */
public class AlignerRunner {
    private static final String ACOUSTIC_MODEL_PATH =
            "resource:/edu/cmu/sphinx/models/en-us/en-us";
    
    private static double Average(List <Double> results) {
    	  Double sum = 0.0;
    	  if(!results.isEmpty()) {
    	    for (Double mark : results) {
    	        sum += mark;
    	    }
    	    return sum.doubleValue() / results.size();
    	  }
    	  return sum;
    }
    
    public static void main(String args[]) throws Exception {
        
    	File dictionaryFile = new File("dictionary/cmudict-en-us.dict");
    	String dictionaryPath = new URL("file:" + dictionaryFile.getAbsolutePath()).toString();
//    	List<String> filebases = new ArrayList<String>(Arrays.asList("filename"));
        List<String> filebases = listFilebases();
        List<Double> results = new ArrayList<Double>();
        for (String filebase : filebases) {
        	String songFilepath = "music/" + filebase + "_vocal.wav";
        	String lyricsFilepath = "lyrics/" + filebase + "_lyrics.txt";
            String outputFilepath = "output/" + filebase + "_timestamp.txt";           
            Double result = align(songFilepath, lyricsFilepath, outputFilepath, dictionaryPath);
            results.add(result); 
            System.out.println("The WER for the song " + filebase + " is " +  result);
        }
        System.out.println("The average WER is " + Average(results));
    }
    
    public static List<String> listFilebases() {
    	List<String> results = new ArrayList<String>();

    	File[] files = new File("music").listFiles();
    	//If this pathname does not denote a directory, then listFiles() returns null. 

    	for (File file : files) {
    	    if (file.isFile()) {
    	    	String filename = file.getName();
    	    	if (filename.contains("_vocal.wav"))
    	        	results.add(filename.substring(0, filename.indexOf("_vocal.wav")));
    	    }
    	}
    	
    	return results;
    }
    
    public static double align(String songFilepath, String lyricsFilepath, String outputFilepath, String dictionaryPath) throws IOException {
    	URL audioUrl;
        
        String lyrics;
        
    	File songFile = new File(songFilepath);
        audioUrl = new URL("file:" + songFile.getAbsolutePath());
        lyrics = new String(Files.readAllBytes(Paths.get(lyricsFilepath)));
        String acousticModelPath = ACOUSTIC_MODEL_PATH;
        String g2pPath = null;
       
        SpeechAligner aligner =
                new SpeechAligner(acousticModelPath, dictionaryPath, g2pPath);

        List<WordResult> results = aligner.align(audioUrl, lyrics);
        List<String> stringResults = new ArrayList<String>();
        for (WordResult wr : results) {
            stringResults.add(wr.getWord().getSpelling());
        }
        
        LongTextAligner textAligner =
                new LongTextAligner(stringResults, 2);
        List<String> words = aligner.getWordExpander().expand(lyrics);

        int[] aid = textAligner.align(words);
        
    	PrintWriter writer = new PrintWriter(outputFilepath, "UTF-8");
        
        int totalCorrect = 0;
        int lastId = -1;

        for (int i = 0; i < aid.length; ++i) {
            if (aid[i] == -1) {
                System.out.format("- %s\n", words.get(i));
                writer.write(words.get(i) + "\n");
            } else {
                if (aid[i] - lastId > 1) {
                    for (WordResult result : results.subList(lastId + 1,
                            aid[i])) {
                        System.out.format("+ %-25s [%s]\n", result.getWord()
                                .getSpelling(), result.getTimeFrame());
                    }
                }
                System.out.format("  %-25s [%s]\n", results.get(aid[i])
                        .getWord().getSpelling(), results.get(aid[i])
                        .getTimeFrame());
                lastId = aid[i];
                writer.write(words.get(i) + "\t" + results.get(aid[i]).getTimeFrame() + "\n");
                totalCorrect++;
            }
            writer.flush();
        }
        writer.write("WER: " + (1 - (totalCorrect * 1.0)/aid.length));
        writer.close();

        if (lastId >= 0 && results.size() - lastId > 1) {
            for (WordResult result : results.subList(lastId + 1,
                    results.size())) {
                System.out.format("+ %-25s [%s]\n", result.getWord()
                        .getSpelling(), result.getTimeFrame());
            }
        }
        return (1 - (totalCorrect * 1.0)/aid.length); 
    }
}
