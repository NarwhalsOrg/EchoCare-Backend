# Use a slim Python image for speed and size
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies for pip and SQLite
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY start.sh .
COPY .env .

# Expose port
EXPOSE 8000

# Start the app
CMD ["bash", "start.sh"]
