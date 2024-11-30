import cv2
import numpy as np

# Переменные для хранения координат ROI
roi_start = None
roi_end = None
drawing = False
track_window = None 
roi_hist = None

smooth_x, smooth_y = 0, 0 
alpha = 0.5

def draw_rectangle(event, x, y, flags, param):
    global roi_start, roi_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN: 
        drawing = True
        roi_start = (x, y) 
        roi_end = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing: 
        roi_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP: 
        drawing = False
        roi_end = (x, y)

# Открытие видео
move = cv2.VideoCapture("/Users/Chulya/Downloads/Vid1.mp4") 

cv2.namedWindow('Select ROI', cv2.WINDOW_NORMAL) 
cv2.setMouseCallback('Select ROI', draw_rectangle)

ret, frame = move.read() 

if not ret:
   print("Видео не захвачено") 
   move.release() 
   cv2.destroyAllWindows()
   exit()

frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

# Цикл для выбора ROI
while True:
    if roi_start and roi_end:
        cv2.rectangle(frame, roi_start, roi_end, (50, 255, 0), 1)

    cv2.imshow('Select ROI', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Обработка выбранного ROI
if roi_start and roi_end:
    x1, y1 = roi_start
    x2, y2 = roi_end
    x, y, w, h = min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1) 
    track_window = (x, y, w, h)
    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Цикл для отслеживания объекта
while True:
    ret, frame = move.read()
    if not ret:
        break

    frame = cv2.resize(frame, (0, 0), fx=1, fy=1) 
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv_frame], [0, 1], roi_hist, [0, 180, 0, 256], 1)
    _, track_window = cv2.meanShift(dst, track_window, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))
    
    x, y, w, h = track_window
    smooth_x = alpha * x + (1 - alpha) * smooth_x 
    smooth_y = alpha * y + (1 - alpha) * smooth_y
    
    cv2.rectangle(frame, (int(smooth_x), int(smooth_y)), (int(smooth_x + w), int(smooth_y + h)), (50, 255, 0), 1)
    cv2.imshow('Frame Mean shift', frame)
    
    if cv2.waitKey(3) & 0xFF == ord('q'): 
        break

move.release() 
cv2.destroyAllWindows()