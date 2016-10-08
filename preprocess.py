import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('board.jpg')
res = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(im_bw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

t = res.copy()
cnt = contours[2]
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

x1 = approx[0][0][0]
y1 = approx[0][0][1]
x2 = approx[2][0][0]
y2 = approx[2][0][1]

#cv2.rectangle(t, (x1,y1), (x2, y2), (0,255,0), thickness=5);

roi = t[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]

cv2.imshow('image', roi)
cv2.waitKey(0)

cv2.destroyAllWindows()
