import cv2
import numpy as np

def butterworth_lowpass_filter(shape, cutoff, order=2):

    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    x = np.linspace(-ccol, ccol - 1, cols)
    y = np.linspace(-crow, crow - 1, rows)
    x, y = np.meshgrid(x, y)
    
    distance = np.sqrt(x**2 + y**2)
    
    bfilter = 1 / (1 + (distance / cutoff)**(2 * order))
    return bfilter

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
image = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg', cv2.IMREAD_GRAYSCALE)

noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
noisy_image = cv2.add(image, noise)


cutoff_frequency = 30
filter_order = 2

butterworth_filter = butterworth_lowpass_filter(noisy_image.shape, cutoff_frequency, filter_order)

image_fft = np.fft.fft2(noisy_image)
image_fft_shifted = np.fft.fftshift(image_fft)

filtered_fft = image_fft_shifted * butterworth_filter

filtered_fft_ishift = np.fft.ifftshift(filtered_fft)
filtered_image = np.fft.ifft2(filtered_fft_ishift)
filtered_image = np.abs(filtered_image)

cv2.imshow('Original Photo', photo_orig) 
cv2.imshow('Noisy', noisy_image)
cv2.imshow('Filtered.jpg', filtered_image.astype(np.uint8))

cv2.waitKey()