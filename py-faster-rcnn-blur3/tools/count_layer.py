#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Test a Fast R-CNN network on an image timeCountbase."""

import _init_paths
from fast_rcnn.test import test_net, _get_blobs
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
import caffe
import argparse
import pprint
import time, os, sys
import cv2
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Test a Fast R-CNN network')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU id to use',
                        default=0, type=int)
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the network',
                        default=None, type=str)
    parser.add_argument('--net', dest='caffemodel',
                        help='model to test',
                        default=None, type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file', default=None, type=str)
    parser.add_argument('--wait', dest='wait',
                        help='wait until net file exists',
                        default=True, type=bool)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='timeCountset to test',
                        default='voc_2007_test', type=str)
    parser.add_argument('--comp', dest='comp_mode', help='competition mode',
                        action='store_true')
    parser.add_argument('--set', dest='set_cfgs',
                        help='set config keys', default=None,
                        nargs=argparse.REMAINDER)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)
    if args.set_cfgs is not None:
        cfg_from_list(args.set_cfgs)

    print('Using config:')
    #pprint.pprint(cfg)

    while not os.path.exists(args.caffemodel) and args.wait:
        print('Waiting for {} to exist...'.format(args.caffemodel))
        time.sleep(10)

    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    net = caffe.Net(args.prototxt, args.caffemodel, caffe.TEST)
    net.name = os.path.splitext(os.path.basename(args.caffemodel))[0]
    '''
    imdb = get_imdb(args.imdb_name)
    imdb.competition_mode(args.comp_mode)

    roidb = imdb.roidb
    i=0
    im = cv2.imread(imdb.image_path_at(i))
    boxes=roidb[i]['boxes']
    blobs, unused_im_scale_factors = _get_blobs(im, boxes)

    if cfg.DEDUP_BOXES > 0:
        v = np.array([1, 1e3, 1e6, 1e9, 1e12])
        hashes = np.round(blobs['rois'] * cfg.DEDUP_BOXES).dot(v)
        _, index, inv_index = np.unique(hashes, return_index=True,
                                        return_inverse=True)
        blobs['rois'] = blobs['rois'][index, :]
        boxes = boxes[index, :]

    # reshape network inputs
    net.blobs['data'].reshape(*(blobs['data'].shape))
    net.blobs['rois'].reshape(*(blobs['rois'].shape))
    data=blobs['data'].astype(np.float32, copy=False)
    '''
    layers=net.layers

    iteration = 10
    layerNum=len(layers)
    timeCount=[0]*layerNum
    for i in range(iteration):
        for j in range(layerNum):
            print "layer:%s"%layers[j]
            time1=time.time()
            net.forward(start=layers[j],end=layers[j])
            timeCount[j]=time.time()-time1
    print layers
    print timeCount
'''
    plt.figure(num=1, figsize=(10,10))
    name=['conv1','conv2','conv3','conv4','conv5','fc6','fc7','bbox','cls']
    data=[sum(timeCount[0:4]),sum(timeCount[4:8]),sum(timeCount[8:10]),sum(timeCount[10:12]),sum(timeCount[12:15]),sum(timeCount[15:18]),sum(timeCount[18:22]),timeCount[23],timeCount[22]+timeCount[24]]
    data=[i*100 for i in data]
    print data
    plt.pie(data,labels=name)
    plt.show()
'''
    #print cls
