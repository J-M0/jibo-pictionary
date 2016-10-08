import cv2
import numpy
import matplotlib.pyplot as plt

img  = cv2.imread('imr.png', cv2.IMREAD_COLOR)
height, width = img.shape[:2]
area = height*width
gray = cv2.imread('imr.png', 0)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 135, 255, cv2.THRESH_BINARY)[1]
#ret,thresh = cv2.threshold(gray,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
x = 0
y = 0
w = 0
h = 0
for cnt in contours:
	#peri = cv2.arcLength(c, True)
	#approx = cv2.approxPolyDP(c, 0.04 * peri, True)
	approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
	area1 = cv2.contourArea(cnt)
	if len(approx)==4 and area1 > 50 and area1 < area*0.95:
		#print "square"
		x,y,w,h = cv2.boundingRect(cnt)
		w = w - 50
		h = h - 50
		x += 25
		y += 25
		print "%s %s %s %s" %(x, y, w, h)
		#cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		#cv2.drawContours(img,[cnt],0,(0,0,255),-1)
crop_img = gray[y:y+h, x:x+w]
plt.imshow(crop_img, cmap='gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.show()