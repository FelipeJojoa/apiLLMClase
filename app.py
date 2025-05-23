from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aiRouter
import os # Importar os para acceder a variables de entorno

# --- Configuración de la Aplicación FastAPI ---
app = FastAPI(
    title="Gemini-like AI System", # Título para la documentación de la API (Swagger UI)
    description="Backend para un sistema de chat con IA generativa utilizando OpenRouter y FastAPI.",
    version="1.0.0",
)

# --- Configuración del Middleware CORS ---
# Permite que el frontend (en un dominio diferente) se comunique con esta API.
# Es crucial para evitar problemas de "Same-Origin Policy" en navegadores.

# Obtener los orígenes permitidos desde una variable de entorno para mayor flexibilidad.
# Si no está definida, se usa un valor por defecto para desarrollo o se restringe.
# En producción, esta variable DEBE estar configurada con la URL exacta del frontend.
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "https://frontai-vpb6.onrender.com").split(',')

print(f"DEBUG: Orígenes CORS permitidos: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Lista de orígenes permitidos
    allow_credentials=True,         # Permitir cookies/credenciales en solicitudes cross-origin
    allow_methods=["*"],            # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Permitir todos los encabezados en las solicitudes
)

# --- Inclusión de Routers de la API ---
# Monta las rutas definidas en aiRouter.py en la aplicación principal.
# Se añade un prefijo a las rutas para mejor organización (e.g., /api/ai-chat)
app.include_router(aiRouter.router, prefix="/api")

# --- Ruta de Inicio (Health Check) ---
@app.get("/", summary="Verificar el estado de la API")
def read_root():
    """
    Endpoint simple para verificar si la API está en funcionamiento.
    """
    return {"message": "API está funcionando correctamente. Visita /docs para la documentación."}

# Otra ruta opcional para un health check más explícito
@app.get("/health", summary="Health Check")
def health_check():
    """
    Realiza un chequeo de salud básico de la API.
    """
    return {"status": "ok", "service": "AI Chat Backend"}