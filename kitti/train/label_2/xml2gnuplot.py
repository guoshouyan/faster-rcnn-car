#!/usr/bin/python
import cPickle as p
import numpy as np

f=open('boxArea.pkl','w')
xaxis = f.load()
yaxis = f.load()

print(xaxis.size());
