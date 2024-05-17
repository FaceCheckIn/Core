import cv2
import mediapipe as mp
import numpy as np
import torch
from PIL import Image
from neuralnet import *


def set_network():
    mp_face_mesh = mp.solutions.face_mesh
    name_backbone_model = 'models/FER_static_ResNet50_AffectNet.pt'
    name_LSTM_model = 'Aff-Wild2'
    pth_backbone_model = ResNet50(7, channels=3)
    pth_backbone_model.load_state_dict(torch.load(name_backbone_model))
    pth_backbone_model.eval()
    pth_LSTM_model = LSTMPyTorch()
    pth_LSTM_model.load_state_dict(torch.load(
        'models/FER_dinamic_LSTM_{0}.pt'.format(name_LSTM_model)))
    pth_LSTM_model.eval()
    DICT_EMO = {0: 'Neutral', 1: 'Happiness', 2: 'Sadness',
                3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger'}

    return mp_face_mesh, pth_backbone_model, pth_LSTM_model, DICT_EMO


def emotion_recognition(image):
    mp_face_mesh, pth_backbone_model, pth_LSTM_model, DICT_EMO = set_network()
    h, w, _ = image.shape
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

        frame_copy = image.copy()
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_copy)
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for fl in results.multi_face_landmarks:
                startX, startY, endX, endY = get_box(fl, w, h)
                cur_face = frame_copy[startY:endY, startX:endX]
                cur_face = pth_processing(Image.fromarray(cur_face))
                features = torch.nn.functional.relu(
                    pth_backbone_model.extract_features(cur_face)).detach().numpy()
                lstm_features = [features] * 10
                lstm_f = torch.from_numpy(np.vstack(lstm_features))
                lstm_f = torch.unsqueeze(lstm_f, 0)
                output = pth_LSTM_model(lstm_f).detach().numpy()
                cl = np.argmax(output)
                label = DICT_EMO[cl]

        return label
