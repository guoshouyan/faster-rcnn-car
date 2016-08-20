label_dir = 'comp4-2730_det_kitti_test2_car.txt';
output_dir = 'result';
fid = fopen(label_dir, 'r');
C  = textscan(fid,'%s %f %f %f %f %f','delimiter', ' ');
fclose(fid);
for i = 1:size(C{1}, 1)
    img_idx = C{1,1}{i,1};
    s = sprintf('%s//%s.txt',output_dir, img_idx);
    fid = fopen(s,'a');
    string = 'Car 0 0 0 ';
    fprintf(fid,'%s',string);
    for j = 3 : 6
        fprintf(fid,'%.2f ',C{1,j}(i,1));
    end
    string2 = '0 0 0 0 0 0 0';
    fprintf(fid,'%s ',string2);
    fprintf(fid,'%.2f\n',C{1,2}(i,1));
    fclose(fid);
end
