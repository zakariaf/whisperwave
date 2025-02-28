import whisper
import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("base")

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Set this in docker-compose.yml

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()

    # Debug: Print request data
    print(f"Received request data: {data}", flush=True)

    file_path = data.get("file_path")
    language = data.get("language", "en")
    transcription_mode = data.get("mode", "local")  # Default to local if not specified

    if not file_path:
        print("❌ Error: Missing `file_path` in request", flush=True)
        return jsonify({"error": "Missing `file_path` in request"}), 400

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist at path: {file_path}", flush=True)
        return jsonify({"error": f"File does not exist at {file_path}"}), 400

    print(f"✅ Processing file: {file_path} with language: {language}, mode: {transcription_mode}", flush=True)

    try:
        if transcription_mode == "local":
            # Use local Whisper model
            result = model.transcribe(file_path, fp16=False, language=language)
            return jsonify({"transcription": result["text"]})
        else:
            # Use OpenAI API
            if not OPENAI_API_KEY:
                return jsonify({"error": "OpenAI API key not configured"}), 500

            # Call OpenAI Whisper API
            with open(file_path, "rb") as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    files={"file": audio_file},
                    data={"model": "whisper-1", "language": language}
                )

            if response.status_code == 200:
                result = response.json()
                return jsonify({"transcription": result["text"]})
            else:
                print(f"OpenAI API Error: {response.text}", flush=True)
                return jsonify({"error": f"OpenAI API error: {response.status_code}"}), 500
    except Exception as e:
        print(f"Transcription Error: {e}", flush=True)
        return jsonify({"error": "Failed to transcribe audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)