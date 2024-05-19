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


def recognition(input_image, employees_faces, employees_identification_codes):
    employees_face_encodings, employees_face_names = encode_known_faces(
        employees_faces, employees_identification_codes)
    matches = face_recognition.compare_faces(
        employees_face_encodings, input_image)
    faceDis = face_recognition.face_distance(
        employees_face_encodings, input_image)
    identification_code = "unknown"
    if True in matches:
        match_index = np.argmin(faceDis)
        identification_code = employees_face_names[match_index]
        return True, identification_code
    return False, identification_code
