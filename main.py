#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:22:20 2022

@author: armin
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


fig, ax = plt.subplots()

img = cv2.imread('/Users/armin/Downloads/IMG_1145.jpg')   # you can read in images with opencv
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
imgGray = cv2.imread('/Users/armin/Downloads/IMG_1145.jpg',0)

"""
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hsv_color1 = np.asarray([40, 40, 0])   
hsv_color2 = np.asarray([255, 255, 255])   

mask = cv2.inRange(img_hsv, hsv_color1, hsv_color2)
"""


plt.imshow(thresh, cmap='gray')   # this colormap will display in black / white
plt.show()


fig.savefig('simple2.svg', format='svg', dpi=3000)



#map a 0-1 matrix of stars
shape = thresh.shape
matrix = np.zeros(shape)
for x in range(0, shape[0]):
    for y in range(0, shape[1]):
        if thresh[x, y] == 255:
            matrix[x, y] = 0
        else:
            matrix[x, y] = 1


#np.savetxt('map.txt',matrix,fmt='%.0f')  #save a matrix of start map

#start of finding islands :)

class Solution:

   def track (self, matrix):
      self.r_len = len(matrix)
      self.c_len = len(matrix[0])
      star_map=[]
      for r in range(self.r_len):
         for c in range(self.c_len):
            if matrix[r][c] == 1:
                self.sum = 0
                self.total = 0
                self.dfs(matrix, r, c)
                #star_map.append([r, c, self.total, self.sum, self.sum/self.total])
                #star_map.append([r, c, self.total])
                star_map.append([r, c, self.sum])
                
      return star_map
      
   def dfs(self, matrix, r, c):
      self.total += 1
      self.sum += imgGray[r][c]
      matrix[r][c] = 0
      if r - 1 >= 0 and matrix[r - 1][c] == 1:
         self.dfs(matrix, r - 1, c)
      if c - 1 >= 0 and matrix[r][c - 1] == 1:
         self.dfs(matrix, r, c - 1)
      if r + 1 < self.r_len and matrix[r + 1][c] == 1:
         self.dfs(matrix, r + 1, c)
      if c + 1 < self.c_len and matrix[r][c + 1] == 1:
         self.dfs(matrix, r, c + 1)
         
ob = Solution()

#SIZE=ob.solve(matrix)
STAR=ob.track(matrix)

#df = pd.DataFrame(STAR ,columns =['X', 'Y', 'val', 'Luminate','L/val' ])
df = pd.DataFrame(STAR ,columns =['X', 'Y', 'val'])

#Export to exel
datatoexcel = pd.ExcelWriter('all.xlsx')
df.to_excel(datatoexcel)
datatoexcel.save()