from crawler import lyrics_search
import glob
import os.path
from format.format import *
from pydub import AudioSegment

def process_songs(file_paths, output_name):
    file_ids = open("output/etc/" + output_name + ".fileids", "w")
    transcription = open("output/etc/" + output_name + ".transcription", "w")
    all_lyrics = open("output/" + output_name + "_all.txt", "w")

    f_file_names = []

    for file_path in glob.glob(file_paths):
        file_name = os.path.basename(file_path)
        f_file_name = format_file_name(file_name)

        print("File path: {}".format(file_path))
        print("File name: {}".format(file_name))
        print("Formatted file name: {}".format(f_file_name))

        if f_file_name in f_file_names:
            print("File with formatted name {} already exists".format(f_file_name))
            continue

        lyrics = lyrics_search.search_by_file_name(file_path)

        if lyrics == None:
            print("Lyrics not found. Skipping song.")
            continue

        f_lyrics = format_lyrics(lyrics)

        transcription_line = "<s> " + f_lyrics + " </s> ({})".format(f_file_name) + "\n\n"
        file_ids_line = output_name + "/" + f_file_name + "\n"

        file_ids.write(file_ids_line)
        transcription.write(transcription_line)

        all_lyrics.write(f_lyrics + " ")

        mp3 = AudioSegment.from_mp3(file_path)
        f_mp3 = mp3.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        f_mp3.export("output/wav/" + output_name + "/" + f_file_name + ".wav", format="wav")

    file_ids.flush()
    file_ids.close()
    transcription.flush()
    transcription.close()
    all_lyrics.flush()
    all_lyrics.close()

    return 0

if __name__ == "__main__":
    process_songs("input/The Essential Bob Dylan/*/0*.mp3", 'bob_dylan_test')




