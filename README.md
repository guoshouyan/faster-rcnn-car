# Use the faster-rcnn to do car detection 
I just upload the code I change from the [faster-rcnn](https://github.com/rbgirshick/py-faster-rcnn)
___
## Tools to use
 1. draw the RCNN network
>./caffe-fast-rcnn/python/draw_net.py models/ZF/faster_rcnn_end2end/test.prototxt test.jpg
 2. time the network
 
 without python layer: 
>./build/tools/caffe time -model ~/fast-rcnn/models/CaffeNet/train.prototxt -gpu 0

 with python layer:
 
 see 'py-faster-rcnn-time', use 'tools/demo2.py --net zf'
___
## Ignore don't care class
you have to ignore both in 'anchor_target_layer' and 'anchor_target_layer'

code in py-faster-rcnn-care
___
## Train faster-rcnn in kitti dataset
code in py-faster-rcnn-blur

data set in kitti/train/label_2
___
## Seperate car and occlude car to two class and train
code in py-faster-rcnn-blur3

data set in kitti/train/label_3
___
## Only rpn network
code in py-faster-rcnn-conv

use the 'demo_rpn.sh' to test the network
 
