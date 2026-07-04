# attendance.py — Face recognition + attendance marking with photo capture
import cv2
import os
import numpy as np
from datetime import datetime
from db import insert_attendance, get_student_name, already_marked_today
from utils import update_excel, update_csv

# ── Ensure folders ── #
os.makedirs("attendance", exist_ok=True)
os.makedirs("trainer", exist_ok=True)
os.makedirs("attendance_photos", exist_ok=True)

TRAINER_PATH = "trainer/trainer.yml"
CONFIDENCE_THRESHOLD = 70   # lower = stricter match
COOLDOWN_SECONDS = 10       # min gap between repeated marks for same student


# ── Load detector and recognizer ── #
def _load_recognizer():
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if not os.path.exists(TRAINER_PATH):
        raise FileNotFoundError(
            "[ERROR] trainer.yml not found. Please train the model first "
            "(Admin Dashboard → Train Model)."
        )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)
    return detector, recognizer


def save_face_photo(face_img, stu_id: int, date: str, time_str: str) -> str:
    """Save the recognised face crop and return its path."""
    safe_time = time_str.replace(":", "-")
    filename = f"attendance_photos/{stu_id}_{date}_{safe_time}.jpg"
    # Resize to a consistent thumbnail
    resized = cv2.resize(face_img, (100, 100))
    cv2.imwrite(filename, resized)
    return filename


def mark_attendance(on_exit_callback=None):
    """
    Opens webcam and marks attendance via face recognition.
    Optionally calls on_exit_callback() when the window is closed.
    """
    print("[INFO] Starting attendance system… Press ESC or close window to stop.")

    try:
        detector, recognizer = _load_recognizer()
    except FileNotFoundError as e:
        print(e)
        return

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        # Try other indices
        for idx in [1, 2]:
            cam = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if cam.isOpened():
                break
        else:
            print("[ERROR] No camera found.")
            return

    last_marked: dict[int, datetime] = {}

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_crop = gray[y:y+h, x:x+w]
            stu_id, confidence = recognizer.predict(face_crop)

            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            if confidence < CONFIDENCE_THRESHOLD:
                name = get_student_name(stu_id) or "Unknown"
                color = (0, 255, 0)
                label = f"{name}  ({int(confidence)})"

                # Cooldown check (don't spam DB on every frame)
                last = last_marked.get(stu_id)
                cooldown_ok = (
                    last is None or
                    (now - last).total_seconds() >= COOLDOWN_SECONDS
                )

                if cooldown_ok and not already_marked_today(stu_id, today):
                    photo_path = save_face_photo(face_crop, stu_id, today, time_str)
                    insert_attendance(stu_id, name, today, time_str,
                                      status="Present", photo_path=photo_path)
                    update_excel(stu_id, name, today, time_str,
                                 status="Present", photo_path=photo_path)
                    update_csv(stu_id, name, today, time_str, status="Present")
                    last_marked[stu_id] = now
                    print(f"[MARKED] {name} (ID:{stu_id}) at {time_str}")

            else:
                color = (0, 0, 255)
                label = "Unknown"

            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

        cv2.putText(img, f"Date: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(img, "Press ESC to exit", (10, img.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Attendance System — Face Recognition", img)

        key = cv2.waitKey(1)
        if key == 27:   # ESC
            break
        # Also stop if the window is closed manually
        if cv2.getWindowProperty(
                "Attendance System — Face Recognition",
                cv2.WND_PROP_VISIBLE) < 1:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("[INFO] Attendance session ended.")
    if on_exit_callback:
        on_exit_callback()


if __name__ == "__main__":
    mark_attendance()
