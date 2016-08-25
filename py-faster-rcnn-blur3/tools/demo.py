#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse
import xml.dom.minidom

CLASSES = ('__background__',
	   'car','carocc')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
	'vgg1024':('VGG_CNN_M_1024',
		   'vgg_cnn_m_1024_faster_rcnn_iter_400000_to8.caffemodel'),
        'zf': ('ZF',
                'zf_faster_rcnn_iter_90000.caffemodel')}

def getGT(image_name):
    if image_name[-3:-1]=='pn':
	dir='/home/crystal/kitti/train/label_2/xml/'
    else:
	dir='/home/crystal/VOCdevkit/VOC2007/Annotations/'
    dir=dir+image_name[0:-3]+'xml'
    DOMTree = xml.dom.minidom.parse(dir)
    objects=DOMTree.getElementsByTagName('object')
    gtBox={}
    for object in objects:
        name=object.getElementsByTagName('name')[0].childNodes[0].nodeValue
        xmin=int(float(object.getElementsByTagName('xmin')[0].childNodes[0].nodeValue))
        ymin=int(float(object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue))
        xmax=int(float(object.getElementsByTagName('xmax')[0].childNodes[0].nodeValue))
        ymax=int(float(object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue))
        bbox=[xmin,ymin,xmax,ymax]
        if name in gtBox:
            gtBox.get(name).append(bbox)
        else:
            gtBox[name]=[bbox]
    return gtBox

def vis_detections(im, class_name, dets, image_name,  thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    
    #gtBox=getGT(image_name)
    #print 'gtBox',': ',gtBox
    #print 'predict: '

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
	print bbox
        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                  fontsize=14)
    '''
    for k,v in gtBox.iteritems():
        for bbox in v:
            ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='green', linewidth=3.5)
            )
            ax.text(bbox[0], bbox[1] - 2,
                '{:s}'.format(k),
            bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')
    '''
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    im_Path = os.path.join(cfg.ROOT_DIR, 'data', 'demo_Output', image_name)
    fig.savefig(im_Path, dpi = fig.dpi)

def demo(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(cfg.ROOT_DIR, '../kitti/train', 'image_2',image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, image_name, thresh=CONF_THRESH)

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    prototxt = os.path.join(cfg.ROOT_DIR, 'models', NETS[args.demo_net][0],
                            'faster_rcnn_end2end', 'test.prototxt')
    caffemodel = os.path.join(cfg.ROOT_DIR, 'output', 'faster_rcnn_end2end', 'kitti_train',
                              NETS[args.demo_net][1])

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    '''
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= im_detect(net, im)
    '''
    '''im_names = ['000007.jpg', '000083.jpg','000091.jpg','000026.jpg',
		'000047.jpg', '000060.jpg']
    '''
    im_names = ['000010.png','000018.png','000017.png','000016.png','000014.png','000015.png']
    for im_name in im_names:
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Demo for data/demo/{}'.format(im_name)
        demo(net, im_name)

    plt.show()
