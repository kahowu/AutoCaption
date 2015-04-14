/*
 * Copyright 1999-2013 Carnegie Mellon University.
 * Portions Copyright 2004 Sun Microsystems, Inc.
 * Portions Copyright 2004 Mitsubishi Electric Research Laboratories.
 * All Rights Reserved.  Use is subject to license terms.
 *
 * See the file "license.terms" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 *
 */
package edu.cmu.sphinx.demo.aligner;

import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import edu.cmu.sphinx.alignment.LongTextAligner;
import edu.cmu.sphinx.api.Configuration;
import edu.cmu.sphinx.api.SpeechAligner;
import edu.cmu.sphinx.api.StreamSpeechRecognizer;
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
public class AlignerDemo {
    private static final String ACOUSTIC_MODEL_PATH =
            "resource:/edu/cmu/sphinx/models/en-us/en-us";
    private static final String DICTIONARY_PATH =
            "resource:/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict";
    private static final String TEXT = "HOW MANY ROADS MUST MAN WALK DOWN BEFORE YOU CALL HIM MAN HOW MANY SEAS MUST WHITE DOVE SAIL BEFORE SHE SLEEPS IN THIS SAND YES AN' HOW MANY TIMES MUST THE CANNON BALLS FLY BEFORE THEY'RE FOREVER BANNED THE ANSWER MY FRIEND IS BLOWING IN THE WIND THE ANSWER IS BLOWING IN THE WIND HOW MANY YEARS CAN MOUNTAIN EXIST BEFORE IT IS WASHED TO THE SEA YES AN' HOW MANY YEARS CAN SOME PEOPLE EXIST BEFORE THEY'RE ALLOWED TO BE FREE YES AN' HOW MANY TIMES MUST MAN TURN HIS HEAD AN' PRETEND THAT HE JUST DOESN'T SEE THE ANSWER MY FRIEND IS BLOWING IN THE WIND AN' THE ANSWER IS BLOWING IN THE WIND HOW MANY TIMES MUST MAN LOOK UP BEFORE HE CAN SEE THE SKY YES AN' HOW MANY EARS MUST ONE MAN HAVE BEFORE HE CAN HEAR PEOPLE CRY YES AN' HOW MANY DEATHS WILL IT TAKE UNTIL HE KNOWS THAT TOO MANY PEOPLE HAVE DIED THE ANSWER MY FRIEND IS BLOWING IN THE WIND THE ANSWER IS BLOWING IN THE WIND";

    public static void main(String args[]) throws Exception {
        URL audioUrl;
        String transcript;
        
        for (String s : args) {
        	System.out.println(s);
        }
        
        if (args.length > 1) {
            audioUrl = new File(args[0]).toURI().toURL();
            Scanner scanner = new Scanner(new File(args[1]));  
            scanner.useDelimiter("\\Z");  
            transcript = scanner.next();
            scanner.close();
        } else {
        	File file = new File("music/test.wav");
            audioUrl = new URL("file:" + file.getAbsolutePath());
            System.out.println(audioUrl);
            System.out.println(audioUrl.getClass());
//            audioUrl = new URL("music/test.wav"); 
//        	System.out.println(System.getProperty("user.dir"));
            transcript = TEXT;
        }
        String acousticModelPath =
                (args.length > 2) ? args[2] : ACOUSTIC_MODEL_PATH;
        String dictionaryPath = (args.length > 3) ? args[3] : DICTIONARY_PATH;
        String g2pPath = (args.length > 4) ? args[4] : null;
       
        SpeechAligner aligner =
                new SpeechAligner(acousticModelPath, dictionaryPath, g2pPath);

        List<WordResult> results = aligner.align(audioUrl, transcript);
        List<String> stringResults = new ArrayList<String>();
        for (WordResult wr : results) {
            stringResults.add(wr.getWord().getSpelling());
        }
        
        LongTextAligner textAligner =
                new LongTextAligner(stringResults, 2);
        List<String> words = aligner.getWordExpander().expand(transcript);

        int[] aid = textAligner.align(words);
        
        int lastId = -1;
        for (int i = 0; i < aid.length; ++i) {
            if (aid[i] == -1) {
                System.out.format("- %s\n", words.get(i));
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
            }
        }

        if (lastId >= 0 && results.size() - lastId > 1) {
            for (WordResult result : results.subList(lastId + 1,
                    results.size())) {
                System.out.format("+ %-25s [%s]\n", result.getWord()
                        .getSpelling(), result.getTimeFrame());
            }
        }
    }
}
