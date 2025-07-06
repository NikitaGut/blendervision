import cv2
import mediapipe as mp

# Инициализация Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Открываем веб-камеру
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Переводим BGR в RGB (Mediapipe работает в RGB)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Обработка изображения
    results = pose.process(img_rgb)

    # Рисуем скелет, если обнаружено тело
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Пример: координаты левой руки
        left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        h, w, _ = frame.shape
        cx, cy = int(left_wrist.x * w), int(left_wrist.y * h)
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

    # Отображение
    cv2.imshow("Mediapipe Pose Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()