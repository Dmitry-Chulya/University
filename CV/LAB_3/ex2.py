import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

smile_start_time = 0
smile_time_threshold = 1.5
smile_detected = False
faces_detected = []  # Список для хранения координат лиц

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Применение двустороннего фильтра для уменьшения шума
    frame = cv2.bilateralFilter(frame, d=2, sigmaColor=100, sigmaSpace=100)

    # Конвертация изображения в черно-белую палитру
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Применение пороговой обработки
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Обнаружение лиц
    faces = face_cascade.detectMultiScale(thresh, scaleFactor=1.05, minNeighbors = 5)

    # Обновление списка лиц
    faces_detected = []
    for (x, y, w, h) in faces:
        faces_detected.append((x, y, w, h))  # Сохраняем координаты лиц

        # Отрисовка прямоугольника вокруг лица
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 255, 0), 1)

        # Обнаружение улыбок в области лица
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors = 5)

        if len(smiles) > 0:
            # Улыбка обнаружена
            if not smile_detected:
                smile_detected = True
                smile_start_time = time.time()  # Запоминаем время начала

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 1)
        else:
            # Улыбка не обнаружена
            if smile_detected:
                # Если улыбка была обнаружена ранее, оставляем рамку
                for (x, y, w, h) in faces_detected:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 255, 0), 1)

                # Сброс состояния улыбки
                smile_detected = False
                smile_start_time = 0  # Обнуляем время

    # Отображение счётчика времени
    if smile_detected:
        elapsed_time = time.time() - smile_start_time  # Вычисляем время улыбки
        cv2.putText(frame, f'Smiling for: {elapsed_time:.1f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Сохранение изображения, если улыбка длится более 1.5 секунд
        if elapsed_time >= smile_time_threshold and elapsed_time < smile_time_threshold + 0.1:
            cv2.imwrite('smile_detected.png', frame)
            cv2.imshow('Smile Detected', frame)
            cv2.waitKey(2000)  # Показать окно 2 секунды
    else:
        cv2.putText(frame, 'Not smiling', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    # Отображение кадра
    cv2.imshow('Smiling test', frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()