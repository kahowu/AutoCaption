% Written by Jeff Wu

% The music folder contains mono original track 
original_music = 'music/*.wav';
files = dir(original_music);

fid = fopen('out.csv', 'w') ;
for i = 1:length(files)
    file_name = files(i).name;
    len = length(file_name);
    save_name = file_name(1:len-4);
    disp(save_name)
    [SDR, SIR, SAR] = rpca_mask_bss(save_name);
    fprintf(fid, '%s,%d,%d,%d\n', save_name, SDR, SIR, SAR) ;
     
end 
fclose(fid);