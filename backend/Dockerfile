# Use Python as base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
