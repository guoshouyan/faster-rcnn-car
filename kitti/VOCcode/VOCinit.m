clear VOCopts
% use VOC2006 or VOC2007 data

VOC2006=false; % set true to use VOC2006 data

% dataset

if VOC2006
    VOCopts.dataset='VOC2006';
else
    VOCopts.dataset='train';
end

% get current directory with forward slashes
cwd=pwd;
cwd(cwd=='\')='/';
fprintf('cwd=%s\n',cwd);
% change this path to point to your copy of the PASCAL VOC data
VOCopts.datadir=[cwd '/'];

% change this path to a writable directory for your results
VOCopts.resdir=[cwd '/results/'];

% change this path to a writable local directory for the example code
VOCopts.localdir=[cwd '/local/' VOCopts.dataset '/'];

% initialize the test set

%VOCopts.testset='val'; % use validation data for development test set
 VOCopts.testset='test'; % use test set for final challenge

% initialize main challenge paths
VOCopts.dontcare='/mnt/data/KITTI/training/label_2/%s.txt';
VOCopts.annopath=[VOCopts.datadir VOCopts.dataset '/label_2/xml/%s.xml'];
VOCopts.imgpath=[VOCopts.datadir VOCopts.dataset '/image_2/%s.jpg'];
VOCopts.imgsetpath=[VOCopts.datadir VOCopts.dataset '/Dataset/%s.txt'];
VOCopts.clsimgsetpath=[VOCopts.datadir VOCopts.dataset '/ImageSets/hello1/%s_%s.txt'];
VOCopts.clsrespath=[VOCopts.resdir 'Mainhello/%s_cls_' VOCopts.testset '_%s.txt'];
VOCopts.detrespath=[VOCopts.resdir '%s_det_kitti_test_%s.txt'];

% initialize segmentation task paths
VOCopts.seg.clsimgpath=[VOCopts.datadir VOCopts.dataset '/SegmentationClass/%s.png'];
VOCopts.seg.instimgpath=[VOCopts.datadir VOCopts.dataset '/SegmentationObject/%s.png'];

VOCopts.seg.imgsetpath=[VOCopts.datadir VOCopts.dataset '/ImageSets/Segmentation/%s.txt'];

VOCopts.seg.clsresdir=[VOCopts.resdir 'Segmentation/%s_%s_cls'];
VOCopts.seg.instresdir=[VOCopts.resdir 'Segmentation/%s_%s_inst'];
VOCopts.seg.clsrespath=[VOCopts.seg.clsresdir '/%s.png'];
VOCopts.seg.instrespath=[VOCopts.seg.instresdir '/%s.png'];

% initialize layout task paths
VOCopts.layout.imgsetpath=[VOCopts.datadir VOCopts.dataset '/ImageSets/Layout/%s.txt'];
VOCopts.layout.respath=[VOCopts.resdir 'Layout/%s_layout_' VOCopts.testset '_%s.xml'];

% initialize the VOC challenge options
if VOC2006
    
    % VOC2006 classes
    
    VOCopts.classes={...
        'bicycle'
        'bus'
        'car'
        'cat'
        'cow'
        'dog'
        'horse'
        'motorbike'
        'person'
        'sheep'};
else

    % VOC2007 classes
    
    VOCopts.classes={...
	'car'
	};
end

VOCopts.nclasses=length(VOCopts.classes);	

VOCopts.poses={...
    'Unspecified'
    'SideFaceLeft'
    'SideFaceRight'
    'Frontal'
    'Rear'};

VOCopts.nposes=length(VOCopts.poses);

VOCopts.parts={...
    'head'
    'hand'
    'foot'};    

VOCopts.maxparts=[1 2 2];   % max of each of above parts

VOCopts.nparts=length(VOCopts.parts);

VOCopts.minoverlap=0.5;

% initialize example options

VOCopts.exannocachepath=[VOCopts.localdir '%s_anno.mat'];

VOCopts.exfdpath=[VOCopts.localdir '%s_fd.mat'];
