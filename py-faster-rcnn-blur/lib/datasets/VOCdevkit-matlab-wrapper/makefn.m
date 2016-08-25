load('error_guo1.mat');
fid = fopen('fn.txt','wt');
for i=1:length(gt)
  for j=1:length(gt(i).det)
    if gt(i).det(j)==0
	BB=gt(i).BB(:,j)';
	fprintf(fid,'%s %d %d %d %d\n',gtids{i},BB(1),BB(2),BB(3),BB(4));
    end
  end
end

