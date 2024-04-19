import cv2
import face_recognition
import numpy as np
import time

known_face_encodings = []
known_face_names = []

def encode_known_faces(image_paths, names):
    for image_path, name in zip(image_paths, names):
        known_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(known_image)
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(known_image, face_locations)
            known_face_encodings.extend(face_encodings)
            known_face_names.extend([name] * len(face_encodings))
        else:
            print("No faces found in:", image_path)


encode_known_faces(["images.jpg","images 3.jpg","newme.jpeg","Dr.Eskandari.jpg"], ["CR7","Messi","Mostafa","DrEskandari"])
video_capture = cv2.VideoCapture(0)

start_time = time.time()


# while True:
while (time.time() - start_time) <= 5:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]


    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)



    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        faceDis = face_recognition.face_distance(known_face_encodings, face_encoding)
        name = "Unknown"


        if True in matches:
            match_index = np.argmin(faceDis)
            name = known_face_names[match_index]
            filename = f"captured_image_{int(time.time() - start_time)}.jpg"
            cv2.imwrite(filename, frame)

        cv2.rectangle(frame, (left+2, top+2), (right+2, bottom+2), (0, 255, 0), 2)
        

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)
        cv2.putText(frame, str(round(min(faceDis),3)), (left , bottom + 16), font, 0.5, (0, 0, 0), 1)

    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
