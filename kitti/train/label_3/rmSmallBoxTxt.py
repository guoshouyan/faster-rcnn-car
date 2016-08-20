#!/usr/bin/python
import os

dir=os.getcwd()
file=os.listdir(dir)

def modifyTXT(filename):
    f=open(filename,'r')
    lines=f.readlines()
    keep=[]
    for line in lines:
        line=line.strip('\n')
        l=line.split(' ')
        if float(l[7])-float(l[5])>25:
            keep.append(line)
    f.close()
    if len(keep)==0:
        os.remove(filename)
    else:
        f=open(filename,'w')
        for line in keep:
            f.write(line)
        f.close()



for filename in file:
    if filename[0]!='.' and filename[-4:-1]=='.tx':
        modifyTXT(filename)

