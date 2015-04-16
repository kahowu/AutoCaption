folder = 'original/';
% v_folder = '/Users/Jeff/Desktop/LM/CC/vocal/';
i_folder = 'output/';
ext = '*.wav';
content = strcat (folder, ext); 
files = dir(content);
% 
for i = 1:length(files)
    file_name = files(i).name;
    len = length(file_name);
    save_name = file_name(1:len-4);
    [data, fs] = audioread (song_name);
    left = data(:,1); 
    right = data(:,2); 
    instrumental = left-right;
%     audiowrite([v_folder ,save_name,'_vocal.wav'],vocal,fs);
    audiowrite([i_folder, save_name,'_instrumental.wav'],instrumental,fs);
end 
