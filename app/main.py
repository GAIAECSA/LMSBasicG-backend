from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as api_router

app = FastAPI()

app = FastAPI(
    title="Backend API Basic LMS",
    description="Backend API para um sistema de gerenciamento de aprendizado (LMS) básico.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "https://midominio.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"msg": "API funcionando 🚀"}