./caffe-fast-rcnn/build/tools/caffe time -model ~/py-faster-rcnn/models/ZF/faster_rcnn_end2end/guotest.prototxt -weights ~/py-faster-rcnn/output/faster_rcnn_end2end/voc_2007_trainval/zf_faster_rcnn_iter_40000.caffemodel -gpu 0 -iterations 10 > temp 2>&1
#./caffe-fast-rcnn/build/tools/caffe time -model ~/fast-rcnn/models/CaffeNet/test.prototxt -weights ~/fast-rcnn/output/default/voc_2007_trainval/caffenet_fast_rcnn_iter_40000_svd_fc6_1024_fc7_256.caffemodel -gpu 0 -iterations 10 > temp 2>&1
grep 'forward:' temp > temp2
#python plot.py
