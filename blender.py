import socket
import mediapipe as mp
import cv2
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
blender_address = ('127.0.0.1', 5055)  # Blender будет слушать здесь

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        landmarks = []
        for lm in results.pose_landmarks.landmark:
            landmarks.append({'x': lm.x, 'y': lm.y, 'z': lm.z})

        # Отправляем координаты в Blender в виде JSON
        message = json.dumps(landmarks).encode('utf-8')
        sock.sendto(message, blender_address)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
sock.close()