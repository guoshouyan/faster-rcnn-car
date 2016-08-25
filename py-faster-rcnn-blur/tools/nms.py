import _init_paths
import cPickle as p 
import numpy as np
from utils.cython_bbox import bbox_overlaps
import os

def nms_proposal(dets,thresh):
    ndets = dets.shape[0]
    suppressed = np.zeros((ndets), dtype=np.int)
    index = 1
    keep = []
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    for i in range(ndets):
        if suppressed[i] >= 1:
            continue
        suppressed[i]=index
        keep.append(i)
        ix1 = x1[i]
        iy1 = y1[i]
        ix2 = x2[i]
        iy2 = y2[i]
        iarea = areas[i]
        for j in range(i + 1, ndets):
            if suppressed[j] >= 1:
                continue
            xx1 = max(ix1, x1[j])
            yy1 = max(iy1, y1[j])
            xx2 = min(ix2, x2[j])
            yy2 = min(iy2, y2[j])
            w = max(0.0, xx2 - xx1 + 1)
            h = max(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (iarea + areas[j] - inter)
            if ovr >= thresh:
                suppressed[j] = index
        index += 1
    return suppressed

def nms_gt(name):
    with open('/home/shouyang/kitti/train/label_2/'+name+'.txt') as f:
        line=f.readlines()
        gt=[l.split(' ')[4:8] for l in line]
    return np.array(gt).astype(np.float)

def compare(name,dets,thresh):
    suppressed=nms_proposal(dets,thresh)
    gt = nms_gt(name)

    overlaps = bbox_overlaps(
            np.ascontiguousarray(dets[:,0:4], dtype=np.float),
            np.ascontiguousarray(gt, dtype=np.float))
    argmax_overlaps = overlaps.argmax(axis=1)
    max_overlaps = overlaps[np.arange(len(overlaps)), argmax_overlaps]
    site = np.where(max_overlaps > 0.5)

    gt_sup=np.array(suppressed)
    gt_sup[site]=(argmax_overlaps[site]+1)*-1
    return suppressed,gt_sup

dir='../nms/'
file=os.listdir(dir)
for filename in file:
    if filename[0]!='.' and filename[-4:-1]=='.pk':
        with open(dir+filename) as f:
            box=p.load(f)
            fc=p.load(f)
            proposal,gt=compare(filename[0:6],box,0.3)
        with open(dir+filename,'w') as f:
            p.dump(box,f)
            p.dump(fc,f)
            p.dump(proposal,f)
            p.dump(gt,f)
        print filename
