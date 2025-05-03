#!/bin/bash

# Activate your virtual environment if needed
# source venv/bin/activate

# Export environment variables (optional, you can use .env directly)
export $(grep -v '^#' .env | xargs)

# Run Alembic migrations (if using Alembic for DB migrations)
# alembic upgrade head

# Start the FastAPI app with Uvicorn and Socket.IO support
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

