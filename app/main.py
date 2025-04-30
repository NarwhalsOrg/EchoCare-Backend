from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routes import users, auth, patients, appointments, prescriptions
from app.core.database import init_db

import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="Healthcare API",
    description="Backend API for Healthcare Application",
    version="1.0.0"
)

# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[os.getenv("ORIGIN")],  # Update this with specific origins in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Initialize database
@app.on_event("startup")
async def startup():
    # Initialize database schema
    await init_db()
    # Test DB connection and print confirmation
    from app.core.database import engine
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")



# Include routers
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
# app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])
# app.include_router(prescriptions.router, prefix="/api/prescriptions", tags=["Prescriptions"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Healthcare API"}