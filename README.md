# WhisperWave 🎙️➡️📝

**AI-Powered Audio Transcription App** using OpenAI's Whisper model.

WhisperWave gives you the **best of both worlds**: process audio files locally using the built-in Whisper model OR leverage OpenAI's API for enhanced accuracy. The choice is yours for each file you upload!

## 🚀 Features
- Upload `.wav`, `.mp3`, `.flac`, `.m4a`, or `.ogg` files and transcribe them into text.
- Select a language before transcription.
- Choose between local Whisper model or OpenAI API while uploading your file.
- Both transcription methods work with all supported audio formats.
- **Translate transcriptions** to multiple languages.
- **Performance analytics** to compare local vs. API transcription.
- View your transcription history and restore previous results.
- Built with **Vue + Flask + Whisper AI**.
- Fully Dockerized with **Docker Compose**.
- Uses **Whisper as a separate service** for scalability.

![WhisperWave Screenshot](screenshot.png)

---

## 📌 Getting Started

### How It Works

1. **Upload your audio file** (.wav, .mp3, .flac, .m4a, or .ogg)
2. **Select your language** (English, German, or other supported languages)
3. **Choose your transcription method**:
   - **Local Whisper**: Process directly on your machine
   - **OpenAI API**: Send to OpenAI for potentially more accurate results
4. **Optionally select a target translation language**
5. **Click "Transcribe"** and get your text!

### 🔹 **1. Clone the Repository**
```bash
git clone https://github.com/zakariaf/whisperwave.git
cd whisperwave
```

### 🔹 **2. Configure OpenAI API Key**
Edit the `docker-compose.yml` file and replace `your_openai_api_key_here` with your actual OpenAI API key:

```yaml
whisper:
  environment:
    - OPENAI_API_KEY=your_openai_api_key_here  # Replace with your API key
```

### 🔹 **3. Run with Docker Compose**
```bash
docker-compose up --build
```

### 🔹 **4. Open in Browser**
- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:5001`
- **Whisper API**: `http://localhost:6000`

---

## 🛠️ Tech Stack
- **Backend**: Flask, Whisper AI (OpenAI)
- **Frontend**: Vue, Vite, Tailwind CSS
- **Containerization**: Docker, Docker Compose
- **Machine Learning**: OpenAI's Whisper for Speech-to-Text
- **Transcription Modes**: Local Whisper model or OpenAI API
- **Translation**: OpenAI GPT API for multilingual support

---

## 🎛️ **Transcription Modes**

### **Local Whisper Model**
- Processes audio files directly on your machine using the containerized Whisper model
- No file size limitations beyond your system's resources
- Works offline without external API dependencies
- Great for larger files or when privacy is a concern

### **OpenAI API**
- Sends your audio file to OpenAI's servers for processing
- Often provides more accurate transcriptions, especially for difficult audio
- Has the following limitations:
  - Maximum file size is 25MB
  - Requires an internet connection
  - Consumes OpenAI API credits

If your file exceeds the 25MB limit for the API mode:
- The application will automatically alert you
- You can simply switch to the local mode instead
- Alternatively, you can compress your audio file or split it into smaller segments

**The choice is yours!** You can easily select which transcription mode to use while uploading your file, giving you the flexibility to choose the best option for each situation.

---

## 🌍 **Translation Feature**

WhisperWave includes support for translating your transcriptions to multiple languages:

### **How It Works**
1. After selecting the source language for your audio, choose a target language for translation (optional)
2. When you transcribe your audio, the text will be automatically translated to your chosen language
3. Both the original transcription and translation will be displayed

### **Supported Languages**
- English, Spanish, French, German, Italian, Portuguese, Dutch
- Russian, Chinese, Japanese, Korean, Arabic, Hindi
- Turkish, Persian/Farsi, and more!

### **Translation Engine**
- Translations are powered by OpenAI's GPT-3.5 Turbo model
- All translations use the OpenAI API regardless of which transcription mode you select
- An OpenAI API key is required for translation functionality

---

## 📊 **Analytics Feature**

WhisperWave includes built-in analytics to help you compare and optimize your transcription workflow:

### **Per-Transcription Analytics**
- Processing time for each transcription
- Model used (base for local, whisper-1 for API)
- Transcription mode (local or API)
- Translation processing time (if applicable)

### **Comparative Analytics**
- Average processing time by mode (local vs. API)
- Usage count for each mode
- Historical performance data
- Model usage statistics

### **Benefits**
- Make data-driven decisions about which mode to use for different files
- Track performance metrics over time
- Compare processing speed between local and API options

Analytics data is stored locally in your browser and is available even after restarting the application.

---

## 📄 API Endpoints (Flask)

### 🎙️ **Transcribe Audio**
```http
POST /transcribe
```

#### **Request (Form Data)**
- `file`: Audio file (.wav, .mp3, .flac, .m4a, .ogg)
- `language`: `en`, `de`, etc.
- `mode`: `local` or `api`
- `target_language`: (Optional) Language code for translation

#### **Response (JSON)**
```json
{
  "transcription": "This is the transcribed text.",
  "translation": "Dies ist der übersetzte Text.",
  "analytics": {
    "processing_time": 4.32,
    "mode": "local",
    "model": "base",
    "translation_time": 1.25
  }
}
```

---

## 📄 API Endpoints (Whisper Service)
Since Whisper is a separate service, the backend **calls it internally**, but you can also call it directly.

### 🎙️ **Direct Whisper Transcription API**
```http
POST /transcribe
```

#### **Request (JSON)**
```json
{
  "file_path": "/uploads/audio.wav",
  "language": "en",
  "mode": "local",
  "target_language": "fr"
}
```

#### **Response (JSON)**
```json
{
  "transcription": "Hello, this is a test.",
  "translation": "Bonjour, c'est un test.",
  "analytics": {
    "processing_time": 3.21,
    "mode": "local",
    "model": "base",
    "translation_time": 1.05
  }
}
```

---

## 🔧 **How to Modify the Whisper Model?**
If you want to use a **different model (e.g., `large` instead of `base`)**, update **`whisper_service/app.py`**:

```python
model = whisper.load_model("large")
```

Then restart:
```bash
docker-compose down
docker-compose up --build
```

---

## 📌 Why is Whisper a Separate Service? 🤔

### **1️⃣ Better Scalability**
- The Whisper service runs independently, allowing **the backend and frontend to scale separately**.
- If multiple users upload audio files, Whisper can **run on its own container without blocking the backend**.

### **2️⃣ Performance Optimization**
- Whisper is a **heavy machine learning model**. Keeping it separate ensures **Flask doesn't slow down** while transcribing audio.
- This setup allows for **future GPU acceleration**, making it faster when deployed in cloud environments.

### **3️⃣ Flexibility for Multiple Models**
- You can deploy **different Whisper models** (`base`, `large`) in separate services.
- The backend can **dynamically select which model to use**, depending on the request.

### **4️⃣ Reusability for Other Applications**
- Other apps (mobile apps, other web services) can **use the Whisper API** without needing to integrate Flask.
- The Whisper service can be deployed **independently** on cloud platforms like **AWS, GCP, or DigitalOcean**.

---

## 🏗️ Future Enhancements
- Implement real-time transcription for streaming audio
- Add **GPU acceleration** for faster local processing
- Add batch processing for multiple files at once
- Create speaker diarization to identify different speakers
- Add audio editing capabilities (trim, cut, etc.) before transcription
- Add custom vocabulary support for domain-specific terminology
- Implement user accounts for cloud synchronization of transcription history
- Deploy to **cloud (AWS, GCP, DigitalOcean)** for global access

---

## 📝 License
MIT License. Free to use and modify.

---

## 💡 **Contributing**
Want to improve **WhisperWave**? Feel free to fork the repository and submit a pull request! 🚀