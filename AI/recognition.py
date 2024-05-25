import face_recognition
import numpy as np


def encode_known_faces(image_paths, identification_codes):
    employees_face_encodings, employees_face_names = [], []
    for image_path, name in zip(image_paths, identification_codes):
        known_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(known_image)
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(
                known_image, face_locations)
            employees_face_encodings.extend(face_encodings)
            employees_face_names.extend([name] * len(face_encodings))
    return employees_face_encodings, employees_face_names


def recognition(detected_face, employees_images: list, emp_identification_codes: list):
    employees_face_encodings, employees_face_names = encode_known_faces(
        employees_images, emp_identification_codes)
    face_locations = face_recognition.face_locations(detected_face)
    encoded_detecting = face_recognition.face_encodings(
        detected_face, face_locations)
    matches = face_recognition.compare_faces(
        employees_face_encodings, encoded_detecting)
    faceDis = face_recognition.face_distance(
        employees_face_encodings, encoded_detecting)
    identification_code = "unknown"
    if True in matches:
        match_index = np.argmin(faceDis)
        identification_code = employees_face_names[match_index]
        return True, identification_code
    return False, identification_code
