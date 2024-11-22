import cv2
import numpy as np


def RGB_to_HSV(pixel):
    pixel = [x / 255 for x in pixel]
    C = [min(pixel), max(pixel)]
    delta = C[1] - C[0]

    H = 0
    if delta == 0:
        H = 0 
    elif C[1] == pixel[2]:
        H = 60 * (((pixel[1] - pixel[0]) / delta) + 6)
    elif C[1] == pixel[1]:
        H = 60 * (((pixel[0] - pixel[2]) / delta) + 2)
    elif C[1] == pixel[0]:
        H = 60 * (((pixel[2] - pixel[1]) / delta) + 4)

    S = 0 if C[1] == 0 else delta / C[1]
    V = C[1]

    return [round(x, 1) for x in [H - 360 if H > 360 else H, S * 100, V * 100]]

def RGB_to_CMYK(pixel):
    pixel = [x / 255 for x in pixel]

    K = 1 - max(pixel)

    C = 0 if K == 1 else (1 - pixel[2] - K)/(1 - K)
    M = 0 if K == 1 else (1 - pixel[1] - K)/(1 - K)
    Y = 0 if K == 1 else (1 - pixel[0] - K)/(1 - K)

    return [round(x * 100) for x in [C, M, Y, K]]

def get_pixel_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_rgb = image[x, y]
        pixel_hsv = RGB_to_HSV(pixel_rgb)
        pixel_cmyk = RGB_to_CMYK(pixel_rgb)

        text_rgb = f'RGB Value: R={pixel_rgb[2]}, G={pixel_rgb[1]}, B={pixel_rgb[0]}'
        text_hsv = f'HSV Value: H={pixel_hsv[0]}, S={pixel_hsv[1]}, V={pixel_hsv[2]}'
        text_cmyk = f'CMYK Value: C={pixel_cmyk[0]}, M={pixel_cmyk[1]}, Y={pixel_cmyk[2]}, K={pixel_cmyk[3]}'



        text_image = np.zeros((500, 1500, 3), dtype=np.uint8)

        cv2.putText(text_image, text_rgb, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(text_image, text_hsv, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(text_image, text_cmyk, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Value", text_image)

image = cv2.imread("/Users/Chulya/Downloads/Jordan.jpg")
print(image.shape)
cv2.namedWindow("Photo")

cv2.setMouseCallback("Photo", get_pixel_value)



while True:
    cv2.imshow("Photo", image)
    if cv2.waitKey(1) & 0xFF == 27: 
        break

cv2.destroyAllWindows()