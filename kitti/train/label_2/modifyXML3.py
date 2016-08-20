#!/usr/bin/python
import xml.dom.minidom
import os
import matplotlib.pyplot as plt
import cPickle as p

def modifyXML(name,countx,county):
	DOMTree = xml.dom.minidom.parse(name)
	objects=DOMTree.getElementsByTagName('object')
	car=[]
	for object in objects:
		if object.getElementsByTagName('name')[0].childNodes[0].nodeValue =='Car':
			xmin=float(object.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
			ymin=float(object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
			xmax=float(object.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
			ymax=float(object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
			bbox=[xmin,ymin,xmax,ymax]
			if ymax-ymin > xmax-xmin:
			    county=county+1
			else:
			    countx=countx+1
	return countx,county

dir=os.getcwd()+'/xml'
file=os.listdir(dir)
countx=0
county=0
for filename in file:
	#print filename
	if filename[0]!='.':
	    countx,county=modifyXML('xml/'+filename,countx,county)
print countx
print county
