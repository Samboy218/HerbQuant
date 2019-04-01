#!/usr/bin/env python3
#written by sam wehunt
#2018-12-09
#Requires the following modules
#	pypng
#	numpy
#	opencv-python
import os
import png
import numpy as np
import cv2

#pixels per inch
resolution = 600
#convert that to mm^2 per pixel
mm2 = (1/(resolution/25.4))**2
for root, dirs, files in os.walk("samples"):
	for name in files:
		print("making BW image of " + os.path.join(root, name))
		leaf = png.Reader(filename=os.path.join(root, name))
		rows, cols, pngdata, d = leaf.read_flat()
		pngdata = np.array(pngdata)
		area = 0

		bwdata = [255 if pngdata[x + (3 - (x % 4))] else 0 for x in range(len(pngdata))]
		'''
		for x, val in enumerate(pngdata):
				ind = x % 4
				if ind == 0:
					continue
				try:
					alpha = pngdata[x + (3 - ind)]
				except:
					print("x: %d" % (x))
					print("ind: %d" % (ind))
					exit()
				if alpha > 0:
					pngdata[x] = 255
				else:
					pngdata[x] = 0
		'''

		png.Writer(alpha='RGBA', height=cols, width=rows).write_array(open('bw.png', 'wb'), bwdata)
		print("BW made")
		print("finding leaf contours...")
		
		im = cv2.imread('bw.png')
		imC = cv2.imread(os.path.join(root, name))
		imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(imgray,127,255,0)
		contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		curr = 1
		for contour in contours:
			area = cv2.contourArea(contour)
			#note: this area could be used to find the leaf area, but contour areas are not quite
			#		the same as the exact pixel count, thus I will calc area later
			if area < 1000:
				continue
			x,y,w,h = cv2.boundingRect(contour)
			roi = imC[y:y+h, x:x+w]
			cv2.imwrite('images/' + os.path.splitext(name)[0] + '-{0:03d}.png'.format(curr), roi)
			curr += 1
		print("found {} contours".format(curr-1))

print("finding area of leaves")
with open("data.csv", "w") as f:
	for root , dirs, files in os.walk("images"):
		for name in files:
			leaf = png.Reader(filename=os.path.join(root, name))
			rows, cols, pngdata, d = leaf.read_flat()
			pixels = [pngdata[n:n+3] for n in range(0, len(pngdata), 3)]
			area = 0
			for pixel in pixels:
				if pixel[0] < 255 or pixel[1] < 255 or pixel[2] < 255:
					area += 1
			print(os.path.join(root, name), round(area*mm2, 3))
			f.write("{},{}\n".format(name, round(area*mm2, 3)))
			
print("wrote leaves to images\\")
print("wrote measurements to data.csv")
