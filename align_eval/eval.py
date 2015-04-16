__author__ = 'Frank'
import os
import numpy as np

CORRECTNESS_THRESHOLD = 0.3 # seconds

def overlap(e_start, e_end, a_start, a_end):
    overlap_duration = max(min(e_end, a_end) - max(e_start, a_start), 0)
    return overlap_duration

def read_timestamp_line(line):
    start = None
    end = None
    line_split = line.split("\t")
    word = line_split[0]

    if len(line_split) > 1:
        time = line_split[1]
        start = int(time.split(":")[0])/1000.
        end = int(time.split(":")[1])/1000.

    return word, start, end

def evaluate(expected_timestamp_filepath, actual_timestamp_filepathpath):
    expected = open(expected_timestamp_filepath, 'r')
    actual = open(actual_timestamp_filepathpath, 'r')

    e_lines = expected.readlines()
    a_lines = actual.readlines()

    word_count = 0
    correct_count = 0

    total_duration = 0
    total_overlap = 0

    for i in range(len(e_lines)):

        e_word, e_start, e_end = read_timestamp_line(e_lines[i].strip("\n"))
        a_word, a_start, a_end = read_timestamp_line(a_lines[i].strip("\n"))
        # if a_word != e_word:
        #     print 'mismatch word', a_word, e_word

        word_duration = e_end - e_start
        total_duration += word_duration

        if a_start == None or e_start == None:

            overlap_duration = 0
        else:
            overlap_duration = overlap(e_start, e_end, a_start, a_end)
            if abs(a_start - e_start) < CORRECTNESS_THRESHOLD and abs(a_end - e_end) < CORRECTNESS_THRESHOLD:
            #print "incorrect word", e_word, a_start, e_start, a_end, e_end
                correct_count += 1

        #print "{}\tExpected: {}-{}\tActual:{}-{}".format(e_word, e_start, e_end, a_start, a_end)
        #print diff

        total_overlap += overlap_duration
        #print overlap_duration

        word_count += 1

    overlap_duration_percentage = total_overlap/total_duration

    return overlap_duration_percentage, 1.*correct_count, 1.*word_count

def audacity_to_timestamp(in_filepath, out_filepath):
    in_file = open(in_filepath, 'r')
    out_file = open(out_filepath, 'w')

    lines = in_file.readlines()[0].split('\r')
    for line in lines:
        line = line.split('\t')

        if len(line) < 3:
            continue
        #print(line)
        start = int(float(line[0]) * 1000)
        end = int(float(line[1]) * 1000)
        word = line[2]

        str = "{}\t{}:{}\n".format(word, start, end)
        out_file.write(str)

    in_file.close()
    out_file.close()

if __name__ == '__main__':
    names = ['segment_01', 'segment_02', 'segment_03', 'segment_04', 'segment_05', \
        'segment_06', 'segment_07', 'segment_08', 'segment_09', 'segment_10']

    #names = ['bw', 'bw1', 'cp1', 'cp2','cp3','cp4', 'ld1','oasis', 'oasis2', 'oasis3']

    overlaps_percentage = []
    corrects = []
    corrects_percentage = []
    words = []

    for name in names:

        in_fp = '../../../Acapella/audacity_marker/{}_timestamp.txt'.format(name)
        out_fp = '../../../Acapella/audacity_output/{}_timestamp.txt'.format(name)
        actual_fp = '../../../Acapella/output/{}_timestamp.txt'.format(name)

        #print(os.getcwd())
        audacity_to_timestamp(in_fp, out_fp)
        overlap_percentage, correct_count, word_count\
            = evaluate(out_fp, actual_fp)

        correct_percentage = correct_count/word_count

        overlaps_percentage.append(overlap_percentage)
        words.append(word_count)
        corrects.append(correct_count)
        corrects_percentage.append(correct_percentage)

        print "{}\tOverlap %: {}\tCorrect Count: {}\tCorrect %: {}".format( \
            name, \
            overlap_percentage, \
            "{}/{}".format(correct_count, word_count), \
            correct_percentage)

    print "Overlap %/song: {}".format(np.mean(overlaps_percentage))
    print "Correct: {}/{}".format(np.sum(corrects),np.sum(words))
    print "Correct %/song: {}".format(np.mean(corrects_percentage))