function res = voc_eval(path, comp_id, test_set, output_dir, rm_res)

VOCopts = get_voc_opts(path);
VOCopts.testset = test_set;

for i = 1:length(VOCopts.classes)
  cls = VOCopts.classes{i};
  voc_eval_cls(cls, VOCopts, comp_id, output_dir, rm_res);
end

function voc_eval_cls(cls, VOCopts, comp_id, output_dir, rm_res)

test_set = VOCopts.testset;
year = VOCopts.dataset(4:end);

addpath(fullfile(VOCopts.datadir, 'VOCcode'));

res_fn = sprintf(VOCopts.detrespath, comp_id, cls);

recall = [];
prec = [];
ap = 0;
ap_auc = 0;

do_eval = true;
if do_eval
  % Bug in VOCevaldet requires that tic has been called first
  VOCclass(VOCopts, comp_id, cls, true,1);
  w = waitforbuttonpress;
  print(gcf, '-djpeg', '-r0', ...
        [output_dir '/' cls '_class.jpg']);
end

rmpath(fullfile(VOCopts.datadir, 'VOCcode'));
