def replace_char(chars, str):
	new_line = str
	for c in chars:
		new_line = new_line.replace(c, '')
	return new_line

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

# def format_music_file_name(music_file_name):
# 	num = range(10)
# 	num_str_arr = map(lambda n: str(n), num)
# 	print(num_str_arr)
# 	new_music = music_file_name.replace(".wav", "")
# 	new_music = replace_char(num_str_arr, new_music)
# 	new_music = replace_char([',', '.', '?', ';', '\'', ':', '!'], new_music)
	
# 	new_music = remove_extra_whitespace(new_music)

# 	new_music = new_music.replace(' ', '-')
# 	new_music = new_music.lower()
# 	return new_music

def format_line(line_str):
	new_line = line_str.upper()
	new_line = replace_char([',', '.', '?', ';', '\'', ':', '!', '(', ')', '\n'], new_line)
	
	new_line = remove_extra_whitespace(new_line)

	return new_line

def format_lyrics(filename):
	file = open(filename, 'r')
	ret = ""
	
	for line in file:
		ret += " " + format_line(line)

	ret = remove_extra_whitespace(ret)

	return ret

def format(lyrics_file_name):
	# if not music_file_name.endswith('.wav'):
		# raise Exception('Music file must have extension .wav!', music_file_name)

	ret = format_lyrics(lyrics_file_name)
	# ret += " " + "(" + format_music_file_name(music_file_name) + ")"
	return ret
