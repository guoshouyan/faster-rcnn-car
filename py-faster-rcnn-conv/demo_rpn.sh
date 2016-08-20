./tools/demo2.py \
  --gpu 0 \
  --def models/ZF/faster_rcnn_end2end/test_rpn.prototxt \
  --net zf \
  --imdb kitti_test \
  --cfg experiments/cfgs/faster_rcnn_end2end.yml

echo "start test"
python ./lib/datasets/VOCdevkit-matlab-wrapper/test.py
