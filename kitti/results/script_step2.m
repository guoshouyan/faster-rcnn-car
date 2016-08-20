length = 7480
label_dir = 'result';
output_dir = 'result';
for img_idx = 0:length
    img_idx
    dir = sprintf('%s/%06d.txt',label_dir,img_idx)
    fid = fopen(dir,'r')
    
    if fid == -1
	'Oops'
        fnew =  fopen(sprintf('%s/%06d.txt',label_dir,img_idx),'w');
        fprintf(fnew, '');
        fclose(fnew);
    
    else
        fclose(fid);
    end
    
end
