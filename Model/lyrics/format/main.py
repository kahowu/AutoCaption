import format
import shutil

if __name__ == '__main__':
	# music_file = 'Blowin\'_In_The_Wind.wav'
	ret = format.format('blowin.txt')
	
	# new_music_file = format.format_music_file_name(music_file) + ".wav"
	
	# if new_music_file != music_file:
		# shutil.copyfile(music_file, new_music_file)

	lyrics_file = open('lyrics.txt', 'w')
	lyrics_file.write(ret)
	lyrics_file.flush()
	lyrics_file.close()

	print(ret)