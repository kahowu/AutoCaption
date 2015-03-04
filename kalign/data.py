# data.py --- 
# 
# Filename: data.py
# Description: 
# Author: Jonathan Chung,
# Maintainer: 
# Created: Tue Mar  3 20:54:11 2015 (-0500)
# Version: 
# Package-Requires: (pydub, pyaudio, ffmpeg, scipy)

# Code:

import pyaudio
from scipy.io import wavfile
import wave
import os

class Kdata():
    '''
    docs
    '''
    required_properties = {"frame_rate": 16,
                           "channels": 1,
                           "no_frames": 16}
    supported_file_types = ["mp3", "ogg", "flv", "mp4", "wma", "aac"]
    def __init__(self, filename):
        filetype = filename[-3:]
        if ".wav" == filetype:
            wave_data, filename = self.read_wav(filename)
        elif filetype in self.supported_file_types:
            wave_data, filename = self.convert_audio_to_wav(filename)
        else:
            raise "Unsupported file"

        self.wave_data = wave_data
        self.filename = filename

    def read_wav(self, filename):
        # Check properties of the wave file
        wav_file = wave.open(filename)
        wav_properties = {"frame_rate": wav_file.getframerate(),
                          "channels": wav_file.getnchannels(),
                          "no_frames": wav_file.getnframes()}

        if self.required_properties == wav_properties:
            wave_data = wavfile.read(filename)
            filename = filename
        else:
            wave_data, filename = self.convert_audio_to_wav(filename)
        return wave_data, filename

    def convert_filename(self, filename):
        path, filename = os.path.split(filename)
        if path == '':
            path = os.getcwd()
        return path + "/_" + filename[0:-3] + "wav"

    def convert_audio_to_wav(self, filename):
        filetype = filename[-3:]
        new_filename = self.convert_filename(filename)
        from pydub import AudioSegment
        supported_file = AudioSegment.from_file(filename, filetype)
        supported_file = supported_file.set_frame_rate(self.required_properties["frame_rate"])
        supported_file = supported_file.set_channels(self.required_properties["channels"])
        # supported_file = supported_file.frame_count(self.required_properties["no_frames"])
        supported_file.export(new_filename, format="wav")
        wave_data = wavfile.read(new_filename)
        filename = new_filename
        return wave_data, filename

    def play(self):
        wav_file = wave.open(self.filename)
        chunk = 1024
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wav_file.getsampwidth()),
            channels=wav_file.getnchannels(),
            rate=wav_file.getframerate(),
            output=True)
        data = wav_file.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wav_file.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

# data.py ends here

if __name__ == "__main__":
    import sys
    import glob
    pathname = sys.argv[1]
    extension_list = map(lambda x: "*." + x, Kdata.supported_file_types)
    os.chdir(pathname)
    for extension in extension_list:
        for video in glob.glob(extension):
            if video[0] == "_":
                continue
            print "Opening filename {0}".format(video)
            Kdata(video)
