import cv2
import numpy as np

def wiener_filter(image, kernel, noise_var, estimated_noise_var):
    image_fft = np.fft.fft2(image)
    kernel_fft = np.fft.fft2(kernel, s=image.shape)
    
    kernel_fft_conj = np.conj(kernel_fft)
    kernel_power = np.abs(kernel_fft) ** 2

    wiener_filter = kernel_fft_conj / (kernel_power + estimated_noise_var)
    wiener_result_fft = wiener_filter * image_fft
    
    wiener_result = np.fft.ifft2(wiener_result_fft)
    
    return np.abs(wiener_result)

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg')
image = cv2.imread("/Users/Chulya/Downloads/Jordan.jpg", cv2.IMREAD_GRAYSCALE)
noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
noisy_image = cv2.add(image, noise)

kernel = np.ones((5, 5), np.float32) / 25

noise_variance = 16
estimated_noise_variance = 8

filtered_image = wiener_filter(noisy_image, kernel, noise_variance, estimated_noise_variance)

cv2.imshow('Original Photo', photo_orig) 
cv2.imshow('noisy_image.jpg', noisy_image)
cv2.imshow('filtered_image.jpg', filtered_image.astype(np.uint8))

cv2.waitKey()