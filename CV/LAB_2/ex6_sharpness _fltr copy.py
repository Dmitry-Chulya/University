import cv2
import numpy as np

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
image = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')


laplacian = cv2.Laplacian(image, cv2.CV_64F)


laplacian = cv2.convertScaleAbs(laplacian)

sharpened_image = cv2.addWeighted(image.astype(np.uint8), 1.5, laplacian, -0.5, 0)

cv2.imshow('Sharpened', sharpened_image)
cv2.imshow('Original Photo', photo_orig) 

cv2.waitKey()