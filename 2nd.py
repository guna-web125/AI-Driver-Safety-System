import cv2
import mediapipe as mp
import numpy as np
import time
import socket

# ===== Raspberry Pi Connection =====
PI_IP = "192.168.137.25"   # 🔴 CHANGE to your Pi IP
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((PI_IP, PORT))

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def eye_aspect_ratio(eye_points, landmarks, frame_w, frame_h):
    points = []

    for p in eye_points:
        lm = landmarks[p]
        x = int(lm.x * frame_w)
        y = int(lm.y * frame_h)
        points.append((x, y))

    if len(points) < 6:
        return 0.3

    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

    return (A + B) / (2.0 * C)


cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.23
DROWSY_TIME = 2

start_time = None
status = "NORMAL"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(LEFT_EYE, landmarks, frame_w, frame_h)
        right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks, frame_w, frame_h)

        ear = (left_ear + right_ear) / 2.0

        if ear < EAR_THRESHOLD:
            if start_time is None:
                start_time = time.time()

            elapsed = time.time() - start_time

            if elapsed > DROWSY_TIME:
                status = "DROWSY"
                client.send(b'D')   # send to Raspberry Pi

                cv2.putText(frame, "DROWSY ALERT!", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        else:
            start_time = None
            status = "NORMAL"

        cv2.putText(frame, f"Status: {status}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
client.close()
