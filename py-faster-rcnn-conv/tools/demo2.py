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
    cfg.TEST.RPN_POST_NMS_TOP_N = 20

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

    imdb = get_imdb(args.imdb_name)
    #imdb.competition_mode(args.comp_mode)
  
    boxes,score,image = imdb_proposals(net, imdb)
    print 'finish detection'
    '''
    rpn_file = 'rpn_proposals.pkl'
    with open(rpn_file, 'wb') as f:
        cPickle.dump(boxes, f, cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(score, f, cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(image, f, cPickle.HIGHEST_PROTOCOL)
    '''
    filename='/home/shouyang/kitti/results/comp4-guo_det_kitti_test_car.txt'
    with open(filename, 'wt') as f:
        for i in range(len(image)):
            for j in range(len(score[i])):
                f.write('{:s} {:.3f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.
                        format(image[i], score[i][j][0],
                        boxes[i][j][0] + 1, boxes[i][j][1] + 1,
                        boxes[i][j][2] + 1, boxes[i][j][3] + 1))
    print 'finish writing'
