#!/bin/bash
set -e

# Run database migrations here if needed

# Start the FastAPI app with Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app
