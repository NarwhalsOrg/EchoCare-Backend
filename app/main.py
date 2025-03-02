import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, patients, appointments, prescriptions
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Healthcare API with FastAPI and Supabase",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(patients.router, prefix="/api", tags=["Patients"])
app.include_router(appointments.router, prefix="/api", tags=["Appointments"])
app.include_router(prescriptions.router, prefix="/api", tags=["Prescriptions"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)