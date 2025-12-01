# face_recognition_module.py
import os
import cv2
from deepface import DeepFace

def load_known_faces(path="known_faces"):
    known_faces = {}
    if not os.path.exists(path):
        os.makedirs(path)
        return known_faces
    for fname in os.listdir(path):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(fname)[0]
            known_faces[name] = os.path.join(path, fname)
    return known_faces

def recognize_faces_in_frame(frame_bgr, known_faces):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    results = []
    for (x, y, w, h) in faces:
        cropped_face = frame_bgr[y:y+h, x:x+w]
        name = "Unknown"
        for known_name, known_path in known_faces.items():
            try:
                result = DeepFace.verify(cropped_face, known_path, model_name="VGG-Face", enforce_detection=False)
                if result["verified"]:
                    name = known_name
                    break
            except Exception as e:
                print(f"Error verifying {known_name}: {e}")
        results.append({"name": name, "bbox": (x, y, w, h)})
    return results
