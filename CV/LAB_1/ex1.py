import cv2
import numpy as np


photo = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
image = photo.copy() 

(h, w) = image.shape[:2]

center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 75, 1.0) 
image = cv2.warpAffine(image, M, (w, h))

image = cv2.resize(image, (int(w * 1.75), int(h * 1.75))) 
(h,w) = image.shape[:2]

image = cv2.line(image, (0, h // 2), (w, h // 2), (0, 255, 0), 10)

cv2.putText(image, '%#?!!a1T', (1000, 100), 

cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

cv2.imshow('Original Photo', photo) 
cv2.imshow('New Image', image)


cv2.waitKey(0)
cv2.destroyAllWindows()

