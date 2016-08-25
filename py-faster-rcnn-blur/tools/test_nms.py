import _init_paths
from fast_rcnn.nms_wrapper import nms
import numpy as np

f=open('/home/shouyang/kitti/results/comp4-guo_det_kitti_test_car.txt')
lines=f.readlines()
f.close()

f=open('/home/shouyang/kitti/results/comp4-guo-compress.txt','w')

count=0
i=0

data=lines[i].strip('\n').split(" ")
name=data[0]
temp=[lines[i]]
det=[map(float,data[2:6]+[data[1]])]
i+=1
while i< len(lines):
    data=lines[i].strip('\n').split(" ")
    if name == data[0]:
        det.append(map(float,data[2:6]+[data[1]]))
        temp.append(lines[i])
    else:
        keep = nms(np.array(det,dtype=np.float32), 0.7)
        count += len(det)-len(keep)
        for t in keep:
            f.write(temp[t])
        det=[map(float,data[2:6]+[data[1]])]
        temp=[lines[i]]
    i+=1

# last image
keep = nms(np.array(det,dtype=np.float32), 0.7)
for t in keep:
    f.write(temp[t])

f.close()

print count
