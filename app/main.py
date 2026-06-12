import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models
from app.api.router import router as api_router

app = FastAPI(
    title="Backend API MDT LMS",
    description="Backend API para um sistema de gerenciamento de aprendizado (LMS) empresarial.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(level=logging.INFO)

os.makedirs("uploads/lesson_blocks", exist_ok=True)
os.makedirs("uploads/courses", exist_ok=True)
os.makedirs("uploads/course_vouchers", exist_ok=True)
os.makedirs("uploads/certificate_templates", exist_ok=True)
os.makedirs("uploads/certificates", exist_ok=True)
os.makedirs("uploads/homework_responses", exist_ok=True)
os.makedirs("uploads/privacy_policies", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"msg": "API funcionando 🚀"}
