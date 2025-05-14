from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.utils.error_handlers import add_custom_error_handlers   # not able to import
from app.routers import predict, chat, diet


app = FastAPI(
    title="Health AI Service",
    description="Diabetes prediction, explainability, chatbot, and diet planning",
    version="1.0.0"
)

# # CORS (adjust origins as needed for your frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with your frontend domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(predict.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(diet.router, prefix="/api")

# Serve static files (for generated PDFs)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add custom error handlers
# add_custom_error_handlers(app)
