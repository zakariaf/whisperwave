import whisper
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()

    # Debug: Print request data
    print(f"Received request data: {data}", flush=True)

    file_path = data.get("file_path")
    language = data.get("language", "en")

    if not file_path:
        print("❌ Error: Missing `file_path` in request", flush=True)
        return jsonify({"error": "Missing `file_path` in request"}), 400

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist at path: {file_path}", flush=True)
        return jsonify({"error": f"File does not exist at {file_path}"}), 400

    print(f"✅ Processing file: {file_path} with language: {language}", flush=True)

    try:
        # Transcribe using the provided language
        result = model.transcribe(file_path, fp16=False, language=language)

        return jsonify({"transcription": result["text"]})
    except Exception as e:
        print(f"Whisper Error: {e}", flush=True)
        return jsonify({"error": "Failed to transcribe audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
