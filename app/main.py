from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from app.routes import users, auth, patients, appointments, prescriptions
from app.core.database import init_db, get_session
from sqlalchemy import text
from sqlalchemy.orm import Session



# remove 
from pydantic import BaseModel
from app.models.model import User
from pydantic import ConfigDict


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



class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}