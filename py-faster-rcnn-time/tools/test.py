import os
import _init_paths
from rpn.proposal_layer import  ProposalLayer
import rpn.proposal_layer

os.system('~/py-faster-rcnn/caffe-fast-rcnn/build/tools/caffe time -model ~/py-faster-rcnn/models/ZF/faster_rcnn_end2end/guotest.prototxt -weights ~/py-faster-rcnn/output/faster_rcnn_end2end/voc_2007_trainval/zf_faster_rcnn_iter_40000.caffemodel -gpu 0 -iterations 10')
