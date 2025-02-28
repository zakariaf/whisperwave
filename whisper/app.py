import whisper
import os
import requests
import json
import mimetypes
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("base")

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Set this in docker-compose.yml

def translate_text(text, target_language, api_key):
    """
    Translate text using OpenAI's GPT model.

    Args:
        text (str): The text to translate
        target_language (str): The target language code
        api_key (str): OpenAI API key

    Returns:
        dict: The translation result with text and processing time
    """
    if not text or not target_language or not api_key:
        return None

    try:
        start_time = time.time()

        # Get the language name from language code for better prompting
        language_names = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "tr": "Turkish",
            "fa": "Persian"
        }

        target_language_name = language_names.get(target_language, target_language)

        # Create the API request for translation
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {target_language_name}. Only respond with the translation, nothing else."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 0.3
            }
        )

        processing_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            translated_text = result['choices'][0]['message']['content'].strip()

            return {
                "text": translated_text,
                "processing_time": processing_time
            }
        else:
            print(f"Translation API Error: {response.text}", flush=True)
            return None

    except Exception as e:
        print(f"Translation Error: {e}", flush=True)
        return None

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
            print(f"Using local Whisper model for {file_type} file", flush=True)

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
                translation_result = translate_text(result["text"], target_language, OPENAI_API_KEY)

            response_data = {
                "transcription": result["text"],
                "analytics": {
                    "processing_time": processing_time,
                    "mode": "local",
                    "model": "base"
                }
            }

            if translation_result:
                response_data["translation"] = translation_result["text"]
                response_data["analytics"]["translation_time"] = translation_result["processing_time"]

            return jsonify(response_data)

        else:
            # Use OpenAI API
            if not OPENAI_API_KEY:
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
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
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
                    translation_result = translate_text(result["text"], target_language, OPENAI_API_KEY)

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

                return jsonify(response_data)
            else:
                print(f"OpenAI API Error: {response.text}", flush=True)
                return jsonify({"error": f"OpenAI API error: {response.status_code}"}), 500
    except Exception as e:
        print(f"Transcription Error: {e}", flush=True)
        return jsonify({"error": "Failed to transcribe audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)