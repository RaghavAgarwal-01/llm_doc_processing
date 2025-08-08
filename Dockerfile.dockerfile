# Use a lightweight official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies without cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project files into container working directory
COPY . .

# Expose the port your Flask app will run on (Cloud Run expects 8080 by default)
EXPOSE 8080

# Set environment variable for Python to output logs immediately (optional but useful)
ENV PYTHONUNBUFFERED=1

# Start your Flask app with Gunicorn on port 8080, 4 workers for concurrency
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "api_server:app"]
