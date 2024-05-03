import cv2
import face_recognition
import numpy as np
import time


emloyees_face_encodings = []
emloyees_face_names = []


def encode_known_faces(image_paths, names):
    for image_path, name in zip(image_paths, names):
        known_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(known_image)
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(
                known_image, face_locations)
            emloyees_face_encodings.extend(face_encodings)
            emloyees_face_names.extend([name] * len(face_encodings))


def recognition(detected_face, employees_faces):
    # load face and names from data base
    # employees_face=[]
    # employees_name=[]
    encode_known_faces(employees_face, employees_name)
    matches = face_recognition.compare_faces(
        emloyees_face_encodings, detected_face)
    faceDis = face_recognition.face_distance(
        emloyees_face_encodings, detected_face)
    name = "unknown"
    if True in matches:
        match_index = np.argmin(faceDis)
        name = emloyees_face_names[match_index]

    return True, name
