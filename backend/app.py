import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
WHISPER_URL = "http://whisper:6000/transcribe"  # Whisper Service API URL

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Get language parameter (default to "en" if not provided)
    language = request.form.get("language", "en")

    # Send only the file path to Whisper
    response = requests.post(WHISPER_URL, json={"file_path": file_path, "language": language})

    if response.status_code == 200:
        transcription = response.json()["transcription"]
        return jsonify({"transcription": transcription})
    else:
        return jsonify({"error": "Failed to transcribe"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
