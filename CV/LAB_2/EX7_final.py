import cv2
import numpy as np
import random

# Функция для улучшения качества изображения
def enhance_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

# Функция для создания маркерного изображения
def create_marker_image(binary_image):
    # Создание маркера фона
    markers = np.zeros(binary_image.shape, dtype=np.int32)
    markers[binary_image == 0] = 1
    markers[binary_image == 255] = 2
    return markers


image = cv2.imread('/Users/Chulya/Downloads/test image.png')

# Замена белого фона на черный
white_background = np.all(image >= 240, axis=-1)  # Определение белого фона
image[white_background] = [0, 0, 0]
enhanced_image = enhance_image(image) # Улучшение качества изображения

# Создание двоичного изображения
gray_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

# Применение алгоритма Distance Transform
dist_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 5)

# Нормализация результата
cv2.normalize(dist_transform, dist_transform, 0, 1, cv2.NORM_MINMAX)

# Пороговое преобразование для получения пиков
_, peaks = cv2.threshold(dist_transform, 0.4, 1, cv2.THRESH_BINARY)

# Преобразование изображения для определения маркеров
peaks = np.uint8(peaks * 255)  # Преобразование в 8-битный формат
markers = create_marker_image(peaks)

# Установка маркера фона в верхнем левом углу
markers[0, 0] = 125

# Применение алгоритма Watershed
cv2.watershed(image, markers)

# Создание итогового изображения с цветами
result_image = np.zeros_like(image)
for label in np.unique(markers):
    if label == -1:
        continue  # Игнорирование границ
    mask = np.zeros(markers.shape, dtype=np.uint8)
    mask[markers == label] = 255
    color = [random.randint(0, 255) for _ in range(3)]  # Генерация случайного цвета
    result_image[mask == 255] = color

# Отображение результатов
cv2.imshow('Original Image', image)
cv2.imshow('Enhanced Image', enhanced_image)
cv2.imshow('Binary Image', binary_image)
cv2.imshow('Distance Transform', dist_transform)
cv2.imshow('Watershed Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()