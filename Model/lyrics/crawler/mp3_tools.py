from tools import id3reader

def extractInfo(song):
    id3r = id3reader.Reader(song)

    album = id3r.getValue('album')
    artist = id3r.getValue('performer')
    name = id3r.getValue('title')

    return artist, album, name


