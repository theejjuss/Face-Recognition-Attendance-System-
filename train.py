# train.py — Train LBPH face recognizer from dataset images
import os
import cv2
import numpy as np


def train_model() -> bool:
    dataset_path = "dataset"
    trainer_path = "trainer/trainer.yml"
    os.makedirs("trainer", exist_ok=True)

    if not os.path.isdir(dataset_path) or not os.listdir(dataset_path):
        print("[ERROR] Dataset folder is empty. Register users first.")
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    image_paths = [
        os.path.join(dataset_path, f)
        for f in os.listdir(dataset_path)
        if f.lower().endswith(".jpg")
    ]

    face_samples = []
    ids = []

    for image_path in image_paths:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        filename = os.path.basename(image_path)
        parts = filename.split(".")
        # Expected format: User.<sid>.<name>.<count>.jpg
        if len(parts) < 4:
            continue
        try:
            id_ = int(parts[1])
        except ValueError:
            continue

        faces = face_detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            face_samples.append(img[y:y+h, x:x+w])
            ids.append(id_)

    if not ids:
        print("[ERROR] No face data found in dataset. Register users first.")
        return False

    print(f"[INFO] Training on {len(ids)} face samples for "
          f"{len(set(ids))} student(s)…")
    recognizer.train(face_samples, np.array(ids))
    recognizer.write(trainer_path)
    print(f"[INFO] Model saved to {trainer_path}")
    return True


if __name__ == "__main__":
    train_model()
