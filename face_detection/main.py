import cv2
import threading
import uvicorn
import sys
import os

# ---------------- FIX BACKEND IMPORT ----------------
# Adds project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

#from backend.frame_uploader import upload_driver_frame

# ----------------------------------------------------
from face_detection import FaceDetector
from eye_landmark_extractor import EyeLandmarkExtractor
from drowsiness_detector import DrowsinessDetector
from driver_state_classifier import DriverStateClassifier

from logger import (
    write_state_periodically,
    write_scores_periodically
)

from push_metrics import push_driver_metrics

import Streaming_frames_endpoint as stream
import frame_bridge


# ---------------- INITIALIZE MODULES ----------------
drowsy_detector = DrowsinessDetector()
classifier = DriverStateClassifier()

cap = cv2.VideoCapture(0)
detector = FaceDetector()
extractor = EyeLandmarkExtractor()


# ---------------- START FASTAPI SERVER ----------------
def start_api():
    try:
        print("[INFO] Starting FastAPI streaming server...")

        uvicorn.run(
        stream.app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
        )

    except Exception as e:
        print(f"[ERROR] API Server failed to start: {e}")


# ---------------- MAIN PIPELINE ----------------
def run_face_detection():
    print("🔥 DRIVER MONITORING SYSTEM STARTED")

    while True:
        try:
            ret, frame = cap.read()

            if not ret or frame is None:
                print("[ERROR] Camera frame not received")
                continue

            # --------------------------------------------
            # CREATE CLEAN FRAME COPY FOR DASHBOARD STREAM
            # --------------------------------------------
            raw_frame = frame.copy()

            # Send CLEAN frame to dashboard stream
            try:
                frame_bridge.send_frames(raw_frame)
            except Exception as e:
                print(f"[WARNING] Frame streaming failed: {e}")

            # --------------------------------------------
            # Face detection
            # --------------------------------------------
            data = detector.detect(frame)
            face_detected = data["face_detected"]

            left_eye = []
            right_eye = []

            landmarks = {
                "left_eye": [],
                "right_eye": []
            }

            x, y, w, h = 0, 0, 0, 0

            # --------------------------------------------
            # Extract eye landmarks
            # --------------------------------------------
            if face_detected:
                try:
                    x, y, w, h = data["face_bbox"]

                    face_region = frame[y:y+h, x:x+w]

                    landmarks = extractor.extract(
                        face_region,
                        (x, y, w, h)
                    )

                    left_eye = landmarks["left_eye"]
                    right_eye = landmarks["right_eye"]

                except Exception as e:
                    print(f"[ERROR] Landmark extraction failed: {e}")
                    face_detected = False

            # --------------------------------------------
            # Classification pipeline
            # --------------------------------------------
            try:

                if face_detected and len(left_eye) == 6 and len(right_eye) == 6:

                    metrics = drowsy_detector.update(
                        left_eye,
                        right_eye
                    )

                    write_scores_periodically(metrics)

                    metrics["face_detected"] = True
                    metrics["eyes_detected"] = True

                    driver_state = classifier.classify(metrics)

                    # Push real-time data to Supabase
                    push_driver_metrics(metrics, driver_state)

                elif face_detected:
                    print("[WARNING] Eye landmarks incomplete")

                    metrics = {
                        "face_detected": True,
                        "eyes_detected": False,
                        "drowsiness_score": 0,
                        "perclos": 0,
                        "ear": 0,
                        "blink_rate": 0,
                        "avg_closure_duration": 0
                    }

                    driver_state = classifier.classify(metrics)

                else:
                    print("[INFO] Face not detected")

                    metrics = {
                        "face_detected": False,
                        "eyes_detected": False,
                        "drowsiness_score": 0,
                        "perclos": 0,
                        "ear": 0,
                        "blink_rate": 0,
                        "avg_closure_duration": 0
                    }

                    driver_state = classifier.classify(metrics)

            except Exception as e:
                print(f"[ERROR] Classification pipeline failed: {e}")
                driver_state = "ERROR"

            # --------------------------------------------
            # Log final state
            # --------------------------------------------
            try:
                write_state_periodically({
                    "driver_state": driver_state
                })

            except Exception as e:
                print(f"[WARNING] JSON logging failed: {e}")

            print(f"[STATE] {driver_state}")

            # --------------------------------------------
            # LOCAL DEBUG WINDOW ONLY
            # (boxes + landmarks remain here)
            # --------------------------------------------
            if face_detected:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"STATE: {driver_state}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"EAR: {metrics.get('ear', 0):.2f}",
                    (x, y + h + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"PERCLOS: {metrics.get('perclos', 0):.2f}",
                    (x, y + h + 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

                for (lx, ly) in landmarks["left_eye"]:
                    cv2.circle(
                        frame,
                        (lx, ly),
                        3,
                        (0, 0, 255),
                        -1
                    )

                for (rx, ry) in landmarks["right_eye"]:
                    cv2.circle(
                        frame,
                        (rx, ry),
                        3,
                        (255, 0, 0),
                        -1
                    )

            else:
                cv2.putText(
                    frame,
                    f"STATE: {driver_state}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            cv2.imshow("Driver Monitoring System", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                print("[INFO] Exiting system...")
                break

        except Exception as e:
            print(f"[CRITICAL ERROR] Main loop failure: {e}")
            continue

    cap.release()
    cv2.destroyAllWindows()


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    try:
        threading.Thread(
            target=start_api,
            daemon=True
        ).start()

        run_face_detection()

    except KeyboardInterrupt:
        print("[INFO] System stopped manually")

    except Exception as e:
        print(f"[CRITICAL ERROR] System startup failed: {e}")
