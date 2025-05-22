from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter  # o la ruta donde tienes tu router

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontai-vpb6.onrender.com" , "http://127.0.0.1:5500"],  # O especifica ["http://127.0.0.1:5500"] para mayor seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(aiRouter.router)

@app.get("/")
def index():
    return {"message": "API running"}


