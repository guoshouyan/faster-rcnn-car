./tools/test_net.py \
  --gpu 0 \
  --def models/ZF/faster_rcnn_end2end/test.prototxt \
  --net output/faster_rcnn_end2end/kitti_train/zf_faster_rcnn_iter_100000.caffemodel \
  --imdb kitti_test \
  --cfg experiments/cfgs/faster_rcnn_end2end.yml
