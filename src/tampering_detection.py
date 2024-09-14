# src/tampering_detection.py

import cv2
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = 'models/tampering_detection_model.h5'


def load_tampering_model(model_path=MODEL_PATH):
    """
    Load the pre-trained tampering detection model.
    """
    model = load_model(model_path)
    return model


def preprocess_frame(frame, target_size=(224, 224)):
    """
    Preprocess the frame for model prediction.
    """
    frame = cv2.resize(frame, target_size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.astype('float32') / 255.0
    return frame


def detect_tampering(video_path, model, threshold=0.5, frame_sample_rate=30):
    """
    Detect tampering in a video by analyzing frames.
    """
    cap = cv2.VideoCapture(video_path)
    tampered_frames = []
    count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_sample_rate == 0:
            processed = preprocess_frame(frame)
            processed = np.expand_dims(processed, axis=0)
            prediction = model.predict(processed)
            # Assuming model outputs probability of tampering
            if prediction[0][0] > threshold:
                tampered_frames.append(count)
        count += 1
    cap.release()

    tampering_detected = len(tampered_frames) > 0
    return tampering_detected, tampered_frames
