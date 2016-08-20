import numpy as np
import matplotlib.pyplot as plt

fin=open('temp2')
lines=fin.readlines() 
name=[line.split()[4] for line in lines]
data=[float(line.split()[6]) for line in lines]
'''
plt.figure(num=1, figsize=(10,10))
plt.pie(data,labels=name)
plt.show()
'''
plt.figure(num=1, figsize=(10,10))
name2=['conv1','conv2','conv3','conv4','conv5','fc6','fc7','other']
data2=[sum(data[0:4]),sum(data[4:8]),sum(data[8:10]),sum(data[10:12]),sum(data[12:15]),sum(data[15:19]),sum(data[19:24]),sum(data[24:27])]
plt.figure(num=1, figsize=(10,10))
plt.pie(data2,labels=name2)
plt.show()

'''
layer={}
for i in range(len(name)):
	if name[i][-1] in ['1','2','3','4','5','6','7']:
		if name[i][-1] in layer:
			layer[d[-1]]=layer[d[-1]]+[d]
		else:
			layer[d[-1]]=[d]
	else:
		layer[d]=[d]	
print layer
'''
