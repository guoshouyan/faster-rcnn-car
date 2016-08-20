#!/usr/bin/python
import xml.dom.minidom
import os
import matplotlib.pyplot as plt
import cPickle as p
import numpy as np

def modifyXML(name,numCar):
	DOMTree = xml.dom.minidom.parse(name)
	objects=DOMTree.getElementsByTagName('object')
	for object in objects:
		if object.getElementsByTagName('name')[0].childNodes[0].nodeValue =='Car':
			xmin=float(object.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
			ymin=float(object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
			xmax=float(object.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
			ymax=float(object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
                        numCar.append((ymax-ymin)*(xmax-xmin))

dir=os.getcwd()+'/xml'
file=os.listdir(dir)
numCar=[]
for filename in file:
	#print filename
	if filename[0]!='.':
		modifyXML('xml/'+filename,numCar)
num_bins=40
size=len(numCar)
print 'size of numCar = %d'%size

f=open('boxArea.pkl','w')
p.dump(numCar,f)
f.close()

i=0
for x in numCar:
        if x>40000:
                i=i+1
print 'num of car bigger than %d is %d'%(40000,i)
'''
plt.hist(numCar, num_bins,facecolor='blue', alpha=0.5)
plt.show()
'''
