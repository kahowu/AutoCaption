from utils import *

def get_inside(str, start, end):
    start_index = str.find(start)
    end_index = str.find(end)
    if start_index >= 0 or end_index >= 0:
        return str[start_index + len(start):end_index]
    return None

def get_transcription_components(transcription):
    lyrics = get_inside(transcription, "<s> ", " </s>")
    file_name = get_inside(transcription, "(", ")")

    return lyrics, file_name

def format_lyrics(line):
    new_line = line.upper()
    new_line = remove_char(",.:;?!\"<>{}[]!@#$%^&*()", new_line)
    new_line = new_line.replace('\n', ' ')
    new_line = new_line.replace('_', ' ')
    new_line = new_line.replace('-', ' ')
    new_line = remove_extra_whitespace(new_line)

    return new_line

def format_file_name(file_name):

    new_file_name = file_name.lower()
    new_file_name = remove_extension(new_file_name)
    new_file_name = remove_char(',.:;<>?{}[]"\'!@#$%^&*()+', new_file_name)
    new_file_name = remove_extra_whitespace(new_file_name)
    new_file_name = new_file_name.replace(' ', '_')

    return new_file_name
