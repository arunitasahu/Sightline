import os
import cv2
import numpy as np
from deepface import DeepFace
from db import init_db, add_face, get_all_faces, get_face_path

FACES_DIR = os.path.join(os.path.dirname(__file__), '../data/faces')
os.makedirs(FACES_DIR, exist_ok=True)
init_db()

# Register a new face
def register_face(name: str, image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError('Image not found or unreadable')
    # Save image to faces directory
    save_path = os.path.join(FACES_DIR, f"{name}.jpg")
    cv2.imwrite(save_path, img)
    add_face(name, save_path)
    return {"name": name, "image_path": save_path}

# Recognize faces in an image
def recognize_faces(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError('Image not found or unreadable')
    results = []
    for name, face_path in get_all_faces():
        try:
            verification = DeepFace.verify(img1_path=face_path, img2_path=image_path, enforce_detection=False)
            if verification['verified']:
                results.append(name)
        except Exception:
            continue
    return results

# List all registered faces
def list_faces():
    return [name for name, _ in get_all_faces()]
