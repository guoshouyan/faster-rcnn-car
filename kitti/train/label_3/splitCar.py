#!/usr/bin/python
import xml.dom.minidom
import os
import matplotlib.pyplot as plt
import cPickle as p

def modifyXML(name):
	DOMTree = xml.dom.minidom.parse(name)
	objects=DOMTree.getElementsByTagName('object')
	car=[]
	for object in objects:
		if object.getElementsByTagName('name')[0].childNodes[0].nodeValue =='Car':
			occlude=object.getElementsByTagName('occluded')[0].childNodes[0].nodeValue
                        if occlude=='2' or occlude=='1':
                                object.getElementsByTagName('name')[0].childNodes[0].replaceWholeText('CarOcc')
        file=open(name,'w')
	file.write(DOMTree.toxml())

dir=os.getcwd()+'/xml'
file=os.listdir(dir)

for filename in file:
	#print filename
	if filename[0]!='.':
	    modifyXML('xml/'+filename)


