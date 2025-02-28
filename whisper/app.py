import whisper
import os
import requests
import json
import mimetypes
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from translation_service import TranslationService

app = Flask(__name__)
CORS(app)

# Get the Whisper model from environment variable
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
print(f"Loading Whisper model: {WHISPER_MODEL}", flush=True)

# Load Whisper model
try:
    model = whisper.load_model(WHISPER_MODEL)
    print(f"Successfully loaded Whisper model: {WHISPER_MODEL}", flush=True)
except Exception as e:
    print(f"Error loading Whisper model '{WHISPER_MODEL}': {e}", flush=True)
    print("Falling back to 'base' model", flush=True)
    model = whisper.load_model("base")

# Initialize translation service
translation_service = TranslationService()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()

    # Debug: Print request data
    print(f"Received request data: {data}", flush=True)

    file_path = data.get("file_path")
    language = data.get("language", "en")
    transcription_mode = data.get("mode", "local")  # Default to local if not specified
    target_language = data.get("target_language")  # Optional translation language

    # Get the file type (wav or mp3)
    file_type = os.path.splitext(file_path)[1].lower()
    print(f"File type detected: {file_type}", flush=True)

    if not file_path:
        print("❌ Error: Missing `file_path` in request", flush=True)
        return jsonify({"error": "Missing `file_path` in request"}), 400

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist at path: {file_path}", flush=True)
        return jsonify({"error": f"File does not exist at {file_path}"}), 400

    print(f"✅ Processing file: {file_path} with language: {language}, mode: {transcription_mode}", flush=True)

    try:
        translation_result = None

        if transcription_mode == "local":
            # Use local Whisper model - supports both WAV and MP3 directly
            print(f"Using local Whisper model {WHISPER_MODEL} for {file_type} file", flush=True)

            # Start the timer
            start_time = time.time()

            # Perform transcription
            result = model.transcribe(file_path, fp16=False, language=language)

            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"Local processing completed in {processing_time:.2f} seconds", flush=True)

            # If translation is requested
            if target_language and target_language != language:
                print(f"Translating from {language} to {target_language}", flush=True)
                translation_result = translation_service.translate(result["text"], target_language)

            response_data = {
                "transcription": result["text"],
                "analytics": {
                    "processing_time": processing_time,
                    "mode": "local",
                    "model": WHISPER_MODEL
                }
            }

            if translation_result:
                response_data["translation"] = translation_result["text"]
                response_data["analytics"]["translation_time"] = translation_result["processing_time"]
                response_data["analytics"]["translation_model"] = translation_result.get("model", "unknown")

            return jsonify(response_data)

        else:
            # Use OpenAI API
            openai_api_key = os.getenv("OPENAI_API_KEY", "")
            if not openai_api_key:
                return jsonify({"error": "OpenAI API key not configured"}), 500

            # Check file size - OpenAI has a 25MB limit
            file_size = os.path.getsize(file_path)
            if file_size > 25 * 1024 * 1024:  # 25MB in bytes
                print(f"File too large for OpenAI API: {file_size} bytes", flush=True)
                return jsonify({
                    "error": "File exceeds OpenAI's 25MB limit. Please use a smaller file or the local option."
                }), 413

            # Set the correct MIME type for the API request
            mime_types = {
                '.wav': 'audio/wav',
                '.mp3': 'audio/mpeg',
                '.flac': 'audio/flac',
                '.m4a': 'audio/mp4',
                '.ogg': 'audio/ogg'
            }
            file_mime = mime_types.get(file_type, 'audio/wav')  # Default fallback

            print(f"Using OpenAI API for {file_type} file with MIME type: {file_mime}", flush=True)

            # Start the timer
            start_time = time.time()

            # Call OpenAI Whisper API
            with open(file_path, "rb") as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {openai_api_key}"},
                    files={"file": (os.path.basename(file_path), audio_file, file_mime)},
                    data={"model": "whisper-1", "language": language}
                )

            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"API processing completed in {processing_time:.2f} seconds", flush=True)

            if response.status_code == 200:
                result = response.json()

                # If translation is requested
                if target_language and target_language != language:
                    print(f"Translating from {language} to {target_language}", flush=True)
                    translation_result = translation_service.translate(result["text"], target_language)

                response_data = {
                    "transcription": result["text"],
                    "analytics": {
                        "processing_time": processing_time,
                        "mode": "api",
                        "model": "whisper-1"
                    }
                }

                if translation_result:
                    response_data["translation"] = translation_result["text"]
                    response_data["analytics"]["translation_time"] = translation_result["processing_time"]
                    response_data["analytics"]["translation_model"] = translation_result.get("model", "unknown")

                return jsonify(response_data)
            else:
                print(f"OpenAI API Error: {response.text}", flush=True)
                return jsonify({"error": f"OpenAI API error: {response.status_code}"}), 500
    except Exception as e:
        print(f"Transcription Error: {e}", flush=True)
        return jsonify({"error": "Failed to transcribe audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)