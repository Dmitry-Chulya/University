import cv2
import numpy as np

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
image = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg', cv2.IMREAD_GRAYSCALE)

noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
noisy_image = cv2.add(image, noise)

smoothed_image = cv2.blur(noisy_image, (5, 5))

cv2.imshow('Original Photo', photo_orig) 
cv2.imshow('noisy_image.jpg', noisy_image)
cv2.imshow('smoothed_image.jpg', smoothed_image)

cv2.waitKey()