# src/utils.py

import cv2
import os

def extract_frames(video_path, output_dir='temp_frames/', frame_rate=30):
    """
    Extract frames from a video at specified frame rate.
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
