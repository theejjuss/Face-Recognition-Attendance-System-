# register.py — Capture face samples and register student in DB
import cv2
import os
from db import add_student


def register_user(sid: int, name: str, samples: int = 60):
    """
    Capture `samples` face images for the student and save them to dataset/.
    Also persists the student record in the SQLite database.

    sid   : numeric student ID (must be unique)
    name  : student's display name
    """
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        for idx in [1, 2]:
            cam = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if cam.isOpened():
                break
        else:
            print("[ERROR] No camera found.")
            return False

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    count = 0
    print(f"[INFO] Capturing {samples} samples for '{name}' (ID: {sid}). "
          "Look at the camera. Press ESC to cancel.")

    while count < samples:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            filepath = os.path.join(dataset_dir, f"User.{sid}.{name}.{count}.jpg")
            cv2.imwrite(filepath, face_img)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        progress = f"Capturing: {count}/{samples}"
        cv2.putText(img, progress, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(img, f"Student: {name}  ID: {sid}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, "Press ESC to cancel", (10, img.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Register Face — Look at camera", img)

        if cv2.waitKey(1) == 27:
            print("[INFO] Registration cancelled by user.")
            cam.release()
            cv2.destroyAllWindows()
            return False

    cam.release()
    cv2.destroyAllWindows()

    # Save to DB
    add_student(sid, name)
    print(f"[INFO] Registered '{name}' (ID:{sid}) — {count} samples saved.")
    return True
