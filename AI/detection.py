import cv2
import face_recognition
import numpy as np
import time
import datetime


video_capture = cv2.VideoCapture(0)
webcam_on = True
start_time = time.time()

# it should add or replace with after key pressed
# after key pressed it should count to 5 or something
while (time.time() - start_time) <= 5 and webcam_on:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    #check for did a face detect? if len >0 it means that yes! it detected
    if len(face_encodings) > 0:
        detected_time = time.time()
        last_capture_time = time.time()
        
        while (time.time() - detected_time) <= 3.5:
            if time.time() - last_capture_time >= 0.5:
                #capture one image and pass to backend. in code below it captures one image and save to directory
                # cv2.imwrite(f"captured_image_{time.time()}.jpg", frame)
                last_capture_time = time.time()
            if (time.time() - detected_time) >= 3.5:
                webcam_on = False
                break  

                    
        
    # else:
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, "nothing", (50, 50), font, 1.0, (0, 0, 0), 1)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
