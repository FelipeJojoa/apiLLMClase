from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter  # Asegúrate de tener el import correcto

app = FastAPI()

# Agrega aquí el dominio del frontend local o remoto que quieras permitir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontai-vpb6.onrender.com"], # https://frontai-vpb6.onrender.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(aiRouter.router)

@app.get("/")
def index():
    return {"message": "API running"}


