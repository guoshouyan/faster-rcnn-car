#!/usr/bin/python
import xml.dom.minidom
import os
import matplotlib.pyplot as plt
import cPickle as p
import numpy as np

def modifyXML(name,xaxis,yaxis):
	DOMTree = xml.dom.minidom.parse(name)
	objects=DOMTree.getElementsByTagName('object')
	for object in objects:
		if object.getElementsByTagName('name')[0].childNodes[0].nodeValue =='Car':
			xmin=float(object.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
			ymin=float(object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
			xmax=float(object.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
			ymax=float(object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
			xaxis.append(round(xmax-xmin,2))
			yaxis.append(round(ymax-ymin,2))

dir=os.getcwd()+'/xml'
file=os.listdir(dir)
xaxis=[]
yaxis=[]
for filename in file:
	if filename[0]!='.':
		#print filename
		modifyXML('xml/'+filename,xaxis,yaxis)
num_bins=40
f=open('boxArea.pkl','w')
p.dump(xaxis,f)
p.dump(yaxis,f)
f.close()

heatmap, xedges, yedges = np.histogram2d(xaxis, yaxis, num_bins)
extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]
plt.imshow(heatmap,extent=extent)
plt.show()
