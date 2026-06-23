# Use official Python image
FROM python:3.13-slim

# Install ffmpeg (needed for Whisper/audio processing)
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        nodejs \
        npm && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]