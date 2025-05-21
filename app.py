from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter

app = FastAPI()

# Configura CORS correctamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para pruebas. En producción, usa ["https://tusitio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(aiRouter.router)

@app.get("/")
def index():
    return {"message": "API running"}


