import cv2
import numpy as np

photo_orig = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg') 
photo_filter = cv2.imread('/Users/Chulya/Downloads/Jordan.jpg', cv2.IMREAD_GRAYSCALE).astype(float) # Загрузка изображения в градациях серого

rows, cols = photo_filter.shape[:2]
ksize = 8
padsize = int((ksize-1)/2)

# Добавление отступов к изображению для обработки краевых пикселей
pad_img = cv2.copyMakeBorder(photo_filter, *[padsize]*4, cv2.BORDER_DEFAULT)

geomean1 = np.zeros_like(photo_filter)

# Применение геометрического среднего к каждому пикселю изображения
for r in range(rows):
    for c in range(cols):
        geomean1[r, c] = np.prod(pad_img[r:r+ksize, c:c+ksize])**(1/(ksize**2))

# Преобразование результата обратно в 8-битный формат
geomean1 = np.uint8(geomean1)

# Отображение оригинального и преобразованного изображения
cv2.imshow('Original Photo', photo_orig) 
cv2.imshow('Geomean Filter', geomean1)
cv2.waitKey()


