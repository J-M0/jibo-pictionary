import cv2
import numpy as np
from matplotlib import pyplot as plt

def rotateImage(image, angle):
   (h, w) = image.shape[:2]
   center = (w / 2, h / 2)
   M = cv2.getRotationMatrix2D(center,angle,1.0)
   rotated_image = cv2.warpAffine(image, M, (w,h))
   return rotated_image

def process(filename):
    img = cv2.imread(filename)
    res = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(im_bw.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    t = res.copy()
    cnt = contours[2]
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    print cnt.shape
    #x,y,w,h = cv2.boundingRect(cnt)
    #x1 = approx[0][0][0]
    #y1 = approx[0][0][1]
    #x2 = approx[2][0][0]
    #y2 = approx[2][0][1]

    rect = cv2.minAreaRect(cnt)
    angle = rect[2]
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    #print box
    #cv2.drawContours(t,[box],0,(0,0,255),2)
    #print box.shape

    x1 = box[0][0]
    y1 = box[0][1]-20
    x2 = box[2][0]
    y2 = box[2][1]+20

    rot_t = rotateImage(t,angle)
    rot_c = rot_t[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2) ]
    #cv2.rectangle(t, (x1,y1), (x2, y2), (0,255,0), thickness=5)
    #cv2.rectangle(t,(x,y),(x+w,y+h),(0,255,0),2)
    #roi = t[box]
    #print roi.shape
    #cv2.drawContours(t,[cnt],0,(0,0,),-1)
    #rn1 = np.reshape(rn,(17,17,3))
    #print rn1.shape
    #cv2.imshow('image', rot_c)
    #cv2.waitKey(0)

    #cv2.destroyAllWindows()
    return rot_c
