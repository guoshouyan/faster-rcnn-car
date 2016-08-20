#!/usr/bin/python
import xml.dom.minidom
import os
import matplotlib.pyplot as plt
import cPickle as p

def modifyXML(name):
    DOMTree = xml.dom.minidom.parse(name)
    objects=DOMTree.getElementsByTagName('object')
    count=0
    for object in objects:
        ymin=float(object.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
        ymax=float(object.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
       	if ymax-ymin <25:
		DOMTree.getElementsByTagName('annotations')[0].removeChild(object)
        else:
		count+=1
    if count==0:
	os.remove(name)
    else:
        file=open(name,'w')
        file.write(DOMTree.toxml())
        file.close()

dir=os.getcwd()+'/xml'
file=os.listdir(dir)

for filename in file:
    #print filename
    if filename[0]!='.':
        modifyXML('xml/'+filename)

