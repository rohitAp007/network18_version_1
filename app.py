from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess

# Initialize Flask App
app = Flask(__name__)

# Define upload folder for video files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the file upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')  # This serves the HTML file

# Route to handle creator verification
@app.route('/verifyCreator', methods=['POST'])
def verify_creator():
    data = request.json
    creator_id = data.get('creatorId')
    creator_name = data.get('creatorName')
    
    # Simulate verification process (replace this with actual logic)
    if creator_id and creator_name:
        # Simulate verified creator
        return jsonify({"verified": True})
    else:
        return jsonify({"verified": False})

# Route to handle metadata embedding
@app.route('/embedMetadata', methods=['POST'])
def embed_metadata():
    video_file = request.files.get('video')
    creator_id = request.form.get('creatorId')
    original_source = request.form.get('originalSource')

    if not video_file or not creator_id or not original_source:
        return jsonify({"error": "Missing required fields"}), 400

    # Save video file
    if allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(file_path)

        # Simulate metadata embedding (replace this with actual logic)
        metadata = {"creatorId": creator_id, "originalSource": original_source}
        return jsonify({"metadata": metadata})

    return jsonify({"error": "Invalid file type"}), 400

# Route to handle tampering detection
@app.route('/detectTampering', methods=['POST'])
def detect_tampering():
    video_file = request.files.get('video')

    if not video_file:
        return jsonify({"error": "No video uploaded"}), 400

    # Save video file
    if allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(file_path)

        # Simulate tampering detection process (replace with actual logic)
        tampering_detected = False  # Example result
        frames = [100, 150] if tampering_detected else []
        return jsonify({"tampered": tampering_detected, "frames": frames})

    return jsonify({"error": "Invalid file type"}), 400

# Start the Flask web server
if __name__ == '__main__':
    app.run(debug=True)
