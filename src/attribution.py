# src/attribution.py

import cv2
import json
import os

def embed_metadata(video_path, metadata, output_path):
    """
    Embed metadata into video using OpenCV (simple implementation by storing metadata as a separate JSON file).
    """
    metadata_path = os.path.splitext(output_path)[0] + '_metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    print(f"Metadata embedded at {metadata_path}")

def retrieve_metadata(video_path):
    """
    Retrieve metadata associated with the video.
    """
    metadata_path = os.path.splitext(video_path)[0] + '_metadata.json'
    if not os.path.exists(metadata_path):
        return None
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    return metadata

def create_attribution(creator_id, original_source):
    """
    Create attribution metadata.
    """
    return {
        'creator_id': creator_id,
        'original_source': original_source
    }
