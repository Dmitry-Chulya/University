import cv2

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
photo_filtr = cv2.imread("/Users/Chulya/Downloads/Jordan.jpg", cv2.IMREAD_GRAYSCALE)

laplacian = cv2.Laplacian(photo_filtr, cv2.CV_64F)

cv2.imshow('Original Photo', photo_orig) 
cv2.imshow('Laplacian Filter', laplacian)

cv2.waitKey()
