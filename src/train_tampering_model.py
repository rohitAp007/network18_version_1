# src/train_tampering_model.py

import os
import cv2
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

DATA_DIR = 'data/videos/'
MODEL_SAVE_PATH = 'models/tampering_detection_model.h5'

def load_data(data_dir):
    """
    Load video frames and labels.
    Assumes directory structure:
    data/videos/
        tampered/
            video1.mp4
            ...
        not_tampered/
            video2.mp4
            ...
    """
    X = []
    y = []
    classes = ['tampered', 'not_tampered']
    
    for label, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        for video_file in os.listdir(class_dir):
            video_path = os.path.join(class_dir, video_file)
            frames = extract_frames(video_path, frame_rate=30)
            for frame in frames:
                img = cv2.imread(frame)
                if img is not None:
                    img = cv2.resize(img, (224, 224))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    X.append(img)
                    y.append(label)
    X = np.array(X) / 255.0
    y = to_categorical(np.array(y), num_classes=2)
    return X, y

def extract_frames(video_path, output_dir='temp_frames/', frame_rate=30):
    """
    Extract frames from video and save to temporary directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_paths = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_rate == 0:
            frame_path = os.path.join(output_dir, f'{os.path.basename(video_path)}_frame_{count}.jpg')
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
        count += 1
    cap.release()
    return frame_paths

def build_model(input_shape=(224, 224, 3)):
    """
    Build a simple CNN model for tampering detection.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(2, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    X, y = load_data(DATA_DIR)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = build_model()
    model.summary()
    
    model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))
    
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved at {MODEL_SAVE_PATH}")

if __name__ == '__main__':
    main()
