from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import uuid
import werkzeug.utils

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
WHISPER_SERVICE_URL = 'http://whisper:6000/transcribe'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    language = request.form.get('language', 'en')
    mode = request.form.get('mode', 'local')  # Get the transcription mode
    target_language = request.form.get('target_language', '')  # Get optional translation language

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a', '.ogg')):
        # Save file with unique name to prevent conflicts
        extension = os.path.splitext(file.filename)[1].lower()
        filename = str(uuid.uuid4()) + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Call Whisper service
        try:
            request_data = {
                'file_path': file_path,
                'language': language,
                'mode': mode  # Pass the transcription mode
            }

            # Add target_language if it's provided
            if target_language:
                request_data['target_language'] = target_language

            response = requests.post(
                WHISPER_SERVICE_URL,
                json=request_data
            )

            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({'error': f'Whisper service error: {response.text}'}), 500
        except Exception as e:
            return jsonify({'error': f'Failed to communicate with Whisper service: {str(e)}'}), 500

    return jsonify({'error': 'Only WAV, MP3, FLAC, M4A, and OGG files are supported'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)