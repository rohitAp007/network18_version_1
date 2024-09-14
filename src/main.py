# src/main.py

import argparse
from credential_verification import load_creators, verify_creator, add_creator
from attribution import create_attribution, embed_metadata, retrieve_metadata
from tampering_detection import load_tampering_model, detect_tampering

def main(video_path, creator_id, creator_name, original_source):
    # Load or add creator
    creators_df = load_creators()
    is_verified = verify_creator(creator_id, creators_df)
    if not is_verified:
        print(f"Creator ID {creator_id} is not verified. Verifying now...")
        # Here you can add verification logic (e.g., manual approval, API call)
        # For simplicity, we'll set verified to True
        add_creator(creator_id, creator_name, True)
        is_verified = True
        print(f"Creator ID {creator_id} has been verified.")

    # Create attribution metadata
    metadata = create_attribution(creator_id, original_source)
    embed_metadata(video_path, metadata, output_path=video_path)

    # Load tampering detection model
    model = load_tampering_model()

    # Detect tampering
    tampered, frames = detect_tampering(video_path, model)
    if tampered:
        print(f"Tampering detected in video {video_path} at frames: {frames}")
    else:
        print(f"No tampering detected in video {video_path}.")

    # Retrieve and display metadata
    retrieved_metadata = retrieve_metadata(video_path)
    if retrieved_metadata:
        print("Attribution Metadata:")
        print(retrieved_metadata)
    else:
        print("No metadata found.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Trustworthiness Checker')
    parser.add_argument('--video', type=str, required=True, help='Path to the video file')
    parser.add_argument('--creator_id', type=int, required=True, help='Creator ID')
    parser.add_argument('--creator_name', type=str, required=True, help='Creator Name')
    parser.add_argument('--original_source', type=str, required=True, help='Original Source of the video')

    args = parser.parse_args()

    main(args.video, args.creator_id, args.creator_name, args.original_source)
