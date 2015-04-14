function [] = separation ()

folder = 'music/';
v_folder = 'vocal/';
i_folder = 'instrumental/';
m_folder = 'mix/';
ext = '*.wav';
content = strcat (folder, ext); 
files = dir(content);


for i = 1:length(files)
    file_name = files(i).name;
    len = length(file_name);
    save_name = file_name(1:len-4);
    
    disp(save_name);
    
    song_name = strcat(folder, files(i).name);
    [data, fs] = audioread (song_name);
    instrumental = data(:,1); 
    vocal = data(:,2); 
    mix = instrumental + vocal;
    audiowrite([v_folder ,save_name,'_vocal.wav'],vocal,fs);
    audiowrite([i_folder, save_name,'_instrumental.wav'],instrumental,fs);
    audiowrite([i_folder, save_name,'_mix.wav'],mix,fs);
end 

