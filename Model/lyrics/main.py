from crawler import lyrics_search
import glob
import os.path
from format.format import *

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
        f_lyrics = format_lyrics(lyrics)

        transcription_line = f_lyrics + " ({})".format(f_file_name) + "\n"
        file_ids_line = output_name + "/" + f_file_name + "\n"

        file_ids.write(file_ids_line)
        transcription.write(transcription_line)

        all_lyrics.write(f_lyrics)

    file_ids.flush()
    file_ids.close()
    transcription.flush()
    transcription.close()
    all_lyrics.flush()
    all_lyrics.close()

    return 0

if __name__ == "__main__":
    process_songs("input/Blonde On Blonde/*.mp3", 'bob_dylan_train')




