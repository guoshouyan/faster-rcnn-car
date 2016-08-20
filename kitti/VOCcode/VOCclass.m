function VOCclass(VOCopts,id,cls,draw,count)
fprintf('this is count %d\n', count);
% load test set
gtids=textread(sprintf(VOCopts.imgsetpath,VOCopts.testset),'%s');

fprintf('imgsetpath=%s\n',VOCopts.imgsetpath);
fprintf('testset=%s\n',VOCopts.testset);
sprintf(VOCopts.imgsetpath,VOCopts.testset)
% load ground truth objects
tic;
npos=0;
gt(length(gtids))=struct('BB',[],'class',[],'diff',[],'det',[]);
for i=1:length(gtids)
    % display progress
    if toc>1
        fprintf('%s: pr: load: %d/%d\n',cls,i,length(gtids));
        drawnow;
        tic;
    end

    %read ground truth
    [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15]= ...
        textread(sprintf(VOCopts.dontcare,gtids{i}),...
    '%s %f %f %f %f %f %f %f %f %f %f %f %f %f %f');
    % extract objects of class
    gt(i).class=a1;
    gt(i).BB=[a5,a6,a7,a8]';
    gt(i).det=false(length(a1),1);
    gt(i).diff=zeros(length(a1),1);
end
fprintf('finish read ground truth\n');
save('guo.mat','gt');

% load results
[ids,confidence,b1,b2,b3,b4]=textread(sprintf(VOCopts.detrespath,id,cls),'%s %f %f %f %f %f');
fprintf('VOCopts.detrespath=%s\n', VOCopts.detrespath);
BB=[b1 b2 b3 b4]';
printf('after read result\n');

% sort detections by decreasing confidence
[sc,si]=sort(-confidence);
ids=ids(si);
BB=BB(:,si);

% assign detections to ground truth objects
nd=length(confidence);
tp=zeros(nd,1);
fp=zeros(nd,1);
tic;

% acculumate number for class
classType={'Car','Cyclist','DontCare','Misc','Pedestrian','Person_sitting','Tram','Truck','Van','nothing'};
classNum=zeros(length(classType),1);

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
                site=strmatch(gt(i).class{jmax},classType,'exact');
                classNum(site)=classNum(site)+1;
            else
                fp(d)=1;            % false positive (multiple detection)
            end
        end
    else
        fp(d)=1;                    % false positive
	classNum(10)=classNum(10)+1;
    end
end
classType
classNum
if draw
    % plot precision/recall
    figure(count);
    bar(classNum);
    set(gca,'XTickLabel',classType);
    %w = waitforbuttonpress;
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

