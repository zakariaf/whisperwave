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

    file_path = data.get("file_path")
    language = data.get("language", "en")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid file path"}), 400

    print(f"Processing file: {file_path} with language: {language}")

    try:
        # Transcribe using the provided language
        result = model.transcribe(file_path, fp16=False, language=language)

        return jsonify({"transcription": result["text"]})
    except Exception as e:
        print(f"Whisper Error: {e}")
        return jsonify({"error": "Failed to transcribe audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
