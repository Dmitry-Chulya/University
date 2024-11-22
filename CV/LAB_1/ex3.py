import cv2 as cv

def apply_filters(img):
    positive_filter = cv.Laplacian(img, cv.CV_64F)
    positive_filter = cv.convertScaleAbs(positive_filter)
    negative_filter =-positive_filter
    return positive_filter, negative_filter

img = cv.imread("/Users/Chulya/Downloads/Jordan.jpg")
positive_filter, negative_filter = apply_filters(img)
cv.imshow("Orig Photo", img)
cv.imshow("Positive", positive_filter)
cv.imshow("Negative", negative_filter)
cv.waitKey(0)
cv.destroyAllWindows()