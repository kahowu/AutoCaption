folder = 'music/';
ext = '*.wav';
content = strcat (folder, ext); 
files = dir(content);

fid = fopen('out.csv', 'w') ;
for i = 1:length(files)
    file_name = files(i).name;
    len = length(file_name);
    save_name = file_name(1:len-4);
    disp(save_name);
    [SDR, SIR, SAR] = rpca_mask_run_fun(save_name);
    fprintf(fid, '%s,%d,%d,%d\n', save_name, SDR, SIR, SAR) ;
    
end 
fclose(fid);