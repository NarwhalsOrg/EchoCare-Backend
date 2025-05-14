FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app
COPY app/data/ ./app/data
COPY start.sh /start.sh
COPY app/static/ ./static/



# Make start.sh executable
RUN chmod +x /start.sh

# Expose port for Uvicorn
EXPOSE 8000

CMD ["/start.sh"]
