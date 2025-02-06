# WhisperWave 🎙️➡️📝
**AI-Powered Audio Transcription App** using OpenAI’s Whisper model.

## 🚀 Features
- Upload `.wav` files and transcribe them into text.
- Select a language before transcription.
- Built with **Vue + Flask + Whisper AI**.
- Fully Dockerized with **Docker Compose**.
- Uses **Whisper as a separate service** for scalability.

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

## 📌 Getting Started

### 🔹 **1. Clone the Repository**
```bash
git clone https://github.com/zakariaf/whisperwave.git
cd whisperwave
```

### 🔹 **2. Run with Docker Compose**
```bash
docker-compose up --build
```

### 🔹 **3. Open in Browser**
- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:5000`
- **Whisper API**: `http://localhost:6000`

---

## 🛠️ Tech Stack
- **Backend**: Flask, Whisper AI (OpenAI)
- **Frontend**: Vue, Vite, Tailwind CSS
- **Containerization**: Docker, Docker Compose
- **Machine Learning**: OpenAI’s Whisper for Speech-to-Text

---

## 📄 API Endpoints (Flask)

### 🎙️ **Transcribe Audio**
```http
POST /transcribe
```

#### **Request (Form Data)**
- `file`: `.wav` file
- `language`: `en`, `es`, `fr`, etc.

#### **Response (JSON)**
```json
{
  "transcription": "This is the transcribed text."
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
  "language": "en"
}
```

#### **Response (JSON)**
```json
{
  "transcription": "Hello, this is a test."
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

## 🏗️ Future Enhancements
- Support for more audio formats.
- Improve UI/UX.
- Implement real-time transcription.
- Add **GPU acceleration** for Whisper.
- Deploy to **cloud (AWS, GCP, DigitalOcean)**.

---

## 📝 License
MIT License. Free to use and modify.

---

## 💡 **Contributing**
Want to improve **WhisperWave**? Feel free to fork the repository and submit a pull request! 🚀
