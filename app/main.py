from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import socketio
import uvicorn

from app.core.config import settings
from app.auth import routes as auth_routes
from app.routes.patient import router as patient_router
from app.service.ChatBot import socketio_events


# Database Setup
from app.core.database import engine, Base
from sqlalchemy import text

# Setup Socket.IO Server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"  # Adjust for prod
)
socketio_app = socketio.ASGIApp(sio, static_files={
    '/': './app/static'  # Serve static files (optional)
})

# FastAPI App
app = FastAPI(
    title="Diabetes Chatbot API",
    description="Real-time chatbot for diabetes risk assessment",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(patient_router, prefix="/api", tags=["API"])


# Mount Socket.IO app
app.mount("/", socketio_app)

# Socket.IO Event Handlers (imported from chatbot/socketio_events.py)
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Startup Event
@app.on_event("startup")
async def startup_event():
    print("Starting up...")

    # 1. Create all tables if not exist
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables checked/created.")

        # 2. Test DB connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
