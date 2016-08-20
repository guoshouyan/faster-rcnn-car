function [rec,prec,ap] = VOCevaldet(VOCopts,id,cls,draw,count)
fprintf('this is count %d\n', count);
% load test set
gtids=textread(sprintf(VOCopts.imgsetpath,VOCopts.testset),'%s');
%save('error_guo2.mat','gtids');
fprintf('imgsetpath=%s\n',VOCopts.imgsetpath);
fprintf('testset=%s\n',VOCopts.testset);
sprintf(VOCopts.imgsetpath,VOCopts.testset)
% load ground truth objects
tic;
npos=0;
gt(length(gtids))=struct('BB',[],'diff',[],'det',[], 'dontcare',[]);
for i=1:length(gtids)
    % display progress
    if toc>1
        fprintf('%s: pr: load: %d/%d\n',cls,i,length(gtids));
        drawnow;
        tic;
    end
    
    % read annotation
    rec=PASreadrecord(sprintf(VOCopts.annopath,gtids{i}));

    [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15]= ...
    	textread(sprintf(VOCopts.dontcare,gtids{i}),...
	'%s %f %f %f %f %f %f %f %f %f %f %f %f %f %f');
    % extract objects of class
    clsinds=strmatch(cls,lower({rec.objects(:).class}),'exact');
    gt(i).BB=cat(1,rec.objects(clsinds).bbox)';
    gt(i).diff=zeros(length(clsinds),1);
    gt(i).det=false(length(clsinds),1);
    dc=strmatch('DontCare',a1,'exact');
    gt(i).dontcare=[a5(dc),a6(dc),a7(dc),a8(dc)]';
    npos=npos+sum(~gt(i).diff);
end
fprintf('finish read ground truth\n');
% load results
[ids,confidence,b1,b2,b3,b4]=textread(sprintf(VOCopts.detrespath,id,cls),'%s %f %f %f %f %f');
fprintf('VOCopts.detrespath=%s\n', VOCopts.detrespath);
BB=[b1 b2 b3 b4]';
printf('after read result\n');

% sort detections by decreasing confidence
[sc,si]=sort(-confidence);
ids=ids(si);
BB=BB(:,si);
%save('error_guo1.mat','gtids','gt','cls','ids','confidence');
% assign detections to ground truth objects
nd=length(confidence);
tp=zeros(nd,1);
fp=zeros(nd,1);
tic;

% write fp and fp
fid_tp = fopen('tp.txt','wt');
fid_fp = fopen('fp.txt','wt');

for d=1:nd
    % display progress
    if toc>1
        fprintf('%s: pr: compute: %d/%d\n',cls,d,nd);
        drawnow;
        tic;
    end
    
    % find ground truth image
    i=strmatch(ids{d},gtids,'exact');
    if isempty(i)
	%save('error_guo.mat','ids','d','gtids');
        error('unrecognized image "%s"',ids{d});
    elseif length(i)>1
        error('multiple image "%s"',ids{d});
    end

    % assign detection to ground truth object if any
    bb=BB(:,d);
    ovmax=-inf;
    for j=1:size(gt(i).BB,2)
        bbgt=gt(i).BB(:,j);
        bi=[max(bb(1),bbgt(1)) ; max(bb(2),bbgt(2)) ; min(bb(3),bbgt(3)) ; min(bb(4),bbgt(4))];
        iw=bi(3)-bi(1)+1;
        ih=bi(4)-bi(2)+1;
        if iw>0 & ih>0                
            % compute overlap as area of intersection / area of union
            ua=(bb(3)-bb(1)+1)*(bb(4)-bb(2)+1)+...
               (bbgt(3)-bbgt(1)+1)*(bbgt(4)-bbgt(2)+1)-...
               iw*ih;
            ov=iw*ih/ua;
            if ov>ovmax
                ovmax=ov;
                jmax=j;
            end
        end
    end
    % assign detection as true positive/don't care/false positive
    if ovmax>=VOCopts.minoverlap
        if ~gt(i).diff(jmax)
            if ~gt(i).det(jmax)
                tp(d)=1;            % true positive
		gt(i).det(jmax)=true;
		fprintf(fid_tp,'%d %d %d %d\n',bb(1),bb(2),bb(3),bb(4));
            else
                fp(d)=1;            % false positive (multiple detection)
		fprintf(fid_fp,'%s %d %d %d %d\n',gtids{i},bb(1),bb(2),bb(3),bb(4));
            end
        end
    else
	if ~(find_dontcare(bb, gt(i).dontcare)>=VOCopts.minoverlap)
            fp(d)=1;                    % false positive
	    fprintf(fid_fp,'%s %d %d %d %d\n',gtids{i},bb(1),bb(2),bb(3),bb(4));
        end
    end
end
save('error_guo1.mat','gt','gtids');
fclose(fid_tp);
fclose(fid_fp);
% compute precision/recall
fp=cumsum(fp);
tp=cumsum(tp);
rec=tp/npos;
prec=tp./(fp+tp);

% compute average precision

ap=0;
for t=0:0.1:1
    p=max(prec(rec>=t));
    if isempty(p)
        p=0;
    end
    ap=ap+p/11;
end
save('error_guo2.mat','ap','rec','prec');

if draw
    % plot precision/recall
    figure(count);
    plot(rec,prec,'-');
    grid;
    xlabel 'recall'
    ylabel 'precision'
    title(sprintf('class: %s, subset: %s, AP = %.3f',cls,VOCopts.testset,ap));
end

function ovmax = find_dontcare(bb, dc)
    ovmax=-inf;
    for j=1:size(dc,2)
        bbgt=dc(:,j);
        bi=[max(bb(1),bbgt(1)) ; max(bb(2),bbgt(2)) ; min(bb(3),bbgt(3)) ; min(bb(4),bbgt(4))];
        iw=bi(3)-bi(1)+1;
        ih=bi(4)-bi(2)+1;
        if iw>0 & ih>0
            % compute overlap as area of intersection / area of union
            ua=(bb(3)-bb(1)+1)*(bb(4)-bb(2)+1)+...
               (bbgt(3)-bbgt(1)+1)*(bbgt(4)-bbgt(2)+1)-...
               iw*ih;
            ov=iw*ih/ua;
            if ov>ovmax
                ovmax=ov;
                jmax=j;
            end
        end
    end
