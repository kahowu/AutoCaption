import glob
import lyrics_search


def mass_lyricify(file_path):

    lyrics_file_name = file_name.replace(".mp3", ".txt")
    #print(lyrics)
    lyrics_file = open(lyrics_file_name, "w")

    return 0

if __name__ == "__main__":
    for file_name in glob.glob("music/Blonde On Blonde/*.mp3"):
        print(file_name)
        lyrics_search.lyricify(file_name)


