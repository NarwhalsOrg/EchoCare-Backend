import uvicorn
from app.main import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=os.getenv("HOST"), port=os.getenv("POST"), reload=True)