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
#minimum 'white' value, used for determining what is the paper and what is the leaflets, this needs more investigating
with open("data.csv", "w") as f:
    for root, dirs, files in os.walk("samples"):
        for name in files:
            print("making BW image of " + os.path.join(root, name))
            im_gray = cv2.imread(os.path.join(root, name), cv2.IMREAD_GRAYSCALE)
            (thresh, im_bw) = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            print("BW made")
            print("finding leaf contours...")
            cv2.imwrite("bw.png", im_bw)
            #exit()
            imC = cv2.imread(os.path.join(root, name))
            contours, hierarchy = cv2.findContours(im_bw.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            curr = 1
            for i, contour in enumerate(contours):
                #make sure this contour is not a child (ie a hole in the leaf)
                if hierarchy[0][i][3] != -1:
                    continue
                area = cv2.contourArea(contour)
                #note: this area could be used to find the leaf area, but contour areas are not quite
                #		the same as the exact pixel count, thus I will calc area later
                if area < 1000:
                    continue
                cv2.drawContours(imC, [contour], 0, (255, 255, 0), 1)
                x,y,w,h = cv2.boundingRect(contour)
                roi = imC[y:y+h, x:x+w]
                roi_bw = im_bw[y:y+h, x:x+w]
                #count the number of white pixels in the BW image
                area = np.count_nonzero(roi_bw)
                print(os.path.splitext(name)[0] + '-{0:03d}.png'.format(curr), round(area*mm2, 3))
                f.write("{},{}\n".format(os.path.splitext(name)[0] + '-{0:03d}.png'.format(curr), round(area*mm2, 3)))
                cv2.imwrite('images/' + os.path.splitext(name)[0] + '-{0:03d}.png'.format(curr), roi)
                curr += 1
            print("found {} contours".format(curr-1))
print("wrote leaves to images\\")
print("wrote measurements to data.csv")
