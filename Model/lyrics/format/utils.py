import os.path

def remove_extension(file_name):
    return os.path.splitext(file_name)[0]

def remove_char(chars, str):
    new_line = str
    for c in chars:
        new_line = new_line.replace(c, '')
    return new_line

def normalize_string(str):
    return remove_extra_whitespace(remove_char(",.':;?\"@#$%^&*()-+=<>{}[]", str))

def remove_marginal_whitespace(str):
    if len(str) == 0:
        return str
    if str[0] == ' ':
        str = str[1:]
    if str[len(str) - 1] == ' ':
        str = str[:-1]
    return str


def remove_extra_whitespace(str):
    ret = str
    while '  ' in ret:
        ret = ret.replace('  ', ' ')
    ret = remove_marginal_whitespace(ret)
    return ret
