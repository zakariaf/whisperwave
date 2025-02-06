# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Whisper & dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose API port
EXPOSE 6000

# Run the service
CMD ["python", "app.py"]
