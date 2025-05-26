from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter

app = FastAPI(title="Chat Gemini Dolphin API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar el frontend si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión del router
app.include_router(aiRouter.router)

@app.get("/")
def index():
    return {"message": "API operational"}
