/*
 * Copyright 1999-2004 Carnegie Mellon University.
 * Portions Copyright 2004 Sun Microsystems, Inc.
 * Portions Copyright 2004 Mitsubishi Electric Research Laboratories.
 * All Rights Reserved.  Use is subject to license terms.
 *
 * See the file "license.terms" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 *
 */

package edu.cmu.sphinx.aligner;

import edu.cmu.sphinx.frontend.util.AudioFileDataSource;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;
import edu.cmu.sphinx.linguist.language.grammar.TextAlignerGrammar;

import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;
import java.net.URL;

/**
 * A simple example that shows how to align speech to existing transcription to
 * get times.
 */
public class Aligner {

    public static void main(String[] args) throws IOException, UnsupportedAudioFileException {

        ConfigurationManager cm = new ConfigurationManager("src/edu/cmu/sphinx/config/aligner.xml");
        Recognizer recognizer = (Recognizer) cm.lookup("recognizer");

        TextAlignerGrammar grammar = (TextAlignerGrammar) cm.lookup("textAlignGrammar");
        grammar.setText("testing testing this is a test");
        recognizer.addResultListener(grammar);
        
        /* allocate the resource necessary for the recognizer */
        recognizer.allocate();

        // configure the audio input for the recognizer
        AudioFileDataSource dataSource = (AudioFileDataSource) cm.lookup("audioFileDataSource");
        dataSource.setAudioFile(new URL("file:audio/project.wav"), null);

        Result result;
        while ((result = recognizer.recognize()) != null) {

            String resultText = result.getTimedBestResult(false, true);
            System.out.println(resultText);
        }
    }
}
