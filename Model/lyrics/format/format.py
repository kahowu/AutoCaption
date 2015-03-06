from utils import *


def format_lyrics(line):
    new_line = line.upper()
    new_line = replace_char(",.:;?!\"<>{}[]!@#$%^&*()", new_line)
    new_line = new_line.replace('\n', ' ')
    new_line = remove_extra_whitespace(new_line)

    return new_line


def format_file_name(file_name):

    new_file_name = file_name.lower()
    new_file_name = remove_extension(new_file_name)
    new_file_name = replace_char(',.:;<>?{}[]"\'!@#$%^&*()+', new_file_name)
    new_file_name = remove_extra_whitespace(new_file_name)
    new_file_name = new_file_name.replace(' ', '_')

    return new_file_name
