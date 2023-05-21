from fastapi import FastAPI
from app.domains.router import router as domain_router
from fastapi.middleware.cors import CORSMiddleware
import os

# https://github.com/zhanymkanov/fastapi-best-practices

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(domain_router)

@app.get('/')
def home():
    return {"message": f"welcome to {os.getenv('APP_NAME')} api"}