
########## This script finds the edges of any sort of flow lines with some amount of disturbance
########### and calclates its deviation from the best fit line for that edge. The best fit line can be 
########### taken as per the flow lines and is as per the degree of polynomial being used. In the given examplee 
########### images a single smoke flow is taken giving two edges for which two best fit lines are created and two sets 
########### of cumulative errors of deviation from the best fit line of each edge. 

########## importing required libraries ##########

import numpy as np
import cv2
from matplotlib import pyplot as plt
#from numba import jit

################ load the image to be processed upon and threshold it #############

#Load an color image in grayscale
#img = cv2.imread('image_name.jpg',0)
#t=180

#ret,thresh1 = cv2.threshold(img,t,255,cv2.THRESH_BINARY) 

################## Find the edges of the thresholded image ############

thresh1 = cv2.imread('thresh1.jpg',0) 
edges = cv2.Canny(thresh1,100,200)
edge = 'edge'+'IMG_1955'+'.png'
cv2.imwrite(edge,edges)           # display the edges of the flow lines
cv2.imshow('image',edges)
cv2.waitKey(1000)
cv2.destroyAllWindows()

######################## Initialize necessary variables ###########################

ans = []
yudata = []
xudata = []
xldata = []
yldata = []
cum_error = 0
cum_error1 = 0

###################### finding the x and y coordinates of the edges #####################
ans = np.nonzero(edges)
ans = np.array(ans)
ydata = ans[0]
xdata = ans[1]
xdata = np.array(xdata)
ydata = np.array(ydata)

######### creating a polynomial object for the central line of the two edges #######3

z2 = np.polyfit(xdata, ydata, 2)			
f2 = np.poly1d(z2)
t2 = np.arange(0, edges.shape[1], 1)


######################### splitting the x and y coordinates of the edges into upper and lower coordinates ######

for x in range(len(t2)):
	for y in range(len(ydata)):
		if t2[x] == xdata[y]:
			if f2(x) > ydata[y]:
				yldata = yldata + [ydata[y]]
				xldata = xldata + [xdata[y]]
			elif f2(x) < ydata[y]:
				yudata = yudata + [ydata[y]]
				xudata = xudata + [xdata[y]]			

xudata = np.array(xudata)
yudata = np.array(yudata)
xldata = np.array(xldata)
yldata = np.array(yldata)
print(xudata)
print(len(xudata))
print(yudata)
print(len(yudata))
print(xldata)
print(len(xldata))
print(yldata)
print(len(yldata))

########################## creating polynomial objects ##############################

z = np.polyfit(xudata, yudata, 3)
f = np.poly1d(z)
t = np.arange(0, edges.shape[1], 1)

z1 = np.polyfit(xldata, yldata, 3)
f1 = np.poly1d(z1)
t1 = np.arange(0, edges.shape[1], 1)


############### plotting the best fit lines #################
img = plt.imread("edgeIMG_1955.png")
fig,ax = plt.subplots()
ax.imshow(edges, extent = [0, edges.shape[1], edges.shape[0], 0], cmap="gray")
ax.plot(t, f(t), '-', linewidth=1, color='red')
ax.plot(t1, f1(t), '-', linewidth=1, color='red')
ax.plot(t2, f2(t), '-', linewidth=1, color='red')
plt.show()

############# calculating the cumulative error for the two edges #############33

for x in range( len(t)):
	for y in range (len(xudata)):
		if xudata[y] == t[x]:
			err = (f(x) - yudata[y])
			cum_error = cum_error + err
print ("the error for the upper edge is=")
print(cum_error)

for x in range( len(t1)):
	for y in range (len(xldata)):
		if xldata[y] == t1[x]:
			err1 = (f1(x) - yldata[y])
			cum_error1 = cum_error1 + err1
print ("the error for the lower edge is=")
print(cum_error1)


