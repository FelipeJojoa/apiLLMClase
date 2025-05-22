from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontai-vpb6.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aiRouter.router)

@app.get("/")
def index():
    return {"message": "API running"}


