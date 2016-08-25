#!/usr/bin/env python

# --------------------------------------------------------
# Fast/er/ R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Generate RPN proposals."""

import _init_paths
import numpy as np
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list, get_output_dir
from datasets.factory import get_imdb
from rpn.generate import imdb_proposals,im_proposals
import cPickle
import caffe
import argparse
import pprint
import time, os, sys,cv2

CLASSES = ('__background__',
           'car')

NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'vgg1024':('VGG_CNN_M_1024',
                   'vgg_cnn_m_1024_faster_rcnn_iter_400000_to8.caffemodel'),
        'zf': ('ZF',
                'zf_faster_rcnn_iter_100000.caffemodel')}

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
    parser.add_argument('--net', dest='demo_net',
                        help='model to test',
                        default=None, type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file', default=None, type=str)
    parser.add_argument('--wait', dest='wait',
                        help='wait until net file exists',
                        default=True, type=bool)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='dataset to test',
                        default='voc_2007_test', type=str)
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

    prototxt = os.path.join(cfg.ROOT_DIR, 'models', NETS[args.demo_net][0],
                            'faster_rcnn_end2end', 'test.prototxt')
    caffemodel = os.path.join(cfg.ROOT_DIR, 'output', 'faster_rcnn_end2end', 'kitti_train',NETS[args.demo_net][1])

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)
    if args.set_cfgs is not None:
        cfg_from_list(args.set_cfgs)

    cfg.GPU_ID = args.gpu_id

    # RPN test settings
    cfg.TEST.RPN_PRE_NMS_TOP_N = -1
    cfg.TEST.RPN_POST_NMS_TOP_N = 300

    print('Using config:')
    pprint.pprint(cfg)
    '''
    while not os.path.exists(args.caffemodel) and args.wait:
        print('Waiting for {} to exist...'.format(args.caffemodel))
        time.sleep(10)
    '''
    caffe.set_mode_gpu()
    caffe.set_device(args.gpu_id)
    net = caffe.Net(prototxt,caffemodel, caffe.TEST)
    print '\n\nLoaded network {:s}'.format(caffemodel)
    net.name = os.path.splitext(os.path.basename(caffemodel))[0]

    im_names = ['000010.png','000011.png','000012.png','000013.png','000014.png']
    imdb_boxes = [[] for _ in xrange(len(im_names))]
    score = range(len(im_names))
    for i in range(len(im_names)):
        im_file = os.path.join(cfg.ROOT_DIR, 'data', 'demo', im_names[i])
        im = cv2.imread(im_file)
        #imdb = get_imdb(args.imdb_name)
        imdb_boxes[i],score[i] = im_proposals(net, im)
    print 'imdb_boxes'
    print imdb_boxes

    # output_dir = os.path.dirname(args.caffemodel)
    '''
    output_dir = get_output_dir(imdb, net)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    '''
    rpn_file = os.path.join('/home/shouyang/py-faster-rcnn-blur/tools/output', net.name + '_rpn_proposals.pkl')
    with open(rpn_file, 'wb') as f:
        cPickle.dump(imdb_boxes, f, cPickle.HIGHEST_PROTOCOL)
    print 'Wrote RPN proposals to {}'.format(rpn_file)
