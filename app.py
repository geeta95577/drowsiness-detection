from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
import threading
from playsound import playsound
from utils.eye_utils import eye_aspect_ratio
from utils.mouth_utils import mouth_aspect_ratio

app = Flask(__name__)

# Mediapipe initialization
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]
MOUTH = [78, 308, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 317, 14, 87, 178, 88, 95]

EAR_THRESHOLD = 0.25
ALERT_FRAMES = 10
closed_frames = 0
alarm_playing = False

MAR_THRESHOLD = 0.82
yawn_frames = 0
YAWN_FRAMES = 12


def play_alarm():
    global alarm_playing
    if alarm_playing:
        return
    alarm_playing = True
    try:
        playsound("static/alarm.wav")
    except:
        pass
    alarm_playing = False


def generate_frames():
    global closed_frames, yawn_frames

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:

            mesh_points = np.array([[p.x, p.y] for p in results.multi_face_landmarks[0].landmark])
            h, w, _ = frame.shape
            mesh_points = (mesh_points * [w, h]).astype(int)

            left_EAR = eye_aspect_ratio(mesh_points, LEFT_EYE)
            right_EAR = eye_aspect_ratio(mesh_points, RIGHT_EYE)
            EAR = (left_EAR + right_EAR) / 2.0

            MAR = mouth_aspect_ratio(mesh_points, MOUTH)

            # ----- Yawning -----
            if MAR > MAR_THRESHOLD:
                yawn_frames += 1
            else:
                yawn_frames = 0

            if yawn_frames >= YAWN_FRAMES:
                cv2.putText(frame, "YAWNING!", (80, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 3)

            # ----- Drowsiness -----
            if EAR < EAR_THRESHOLD:
                closed_frames += 1
            else:
                closed_frames = 0

            if closed_frames >= ALERT_FRAMES:
                cv2.putText(frame, "DROWSY!", (80, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                if not alarm_playing:
                    threading.Thread(target=play_alarm, daemon=True).start()
            else:
                cv2.putText(frame, "ACTIVE", (80, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
