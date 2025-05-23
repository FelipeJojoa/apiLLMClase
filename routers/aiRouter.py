import os
import httpx # Importa httpx para manejar excepciones de red y HTTP
from fastapi import APIRouter, HTTPException, status # Importa status para códigos HTTP
from fastapi.responses import JSONResponse
from openai import OpenAI, OpenAIError # Importa OpenAIError para errores específicos de la librería
from dotenv import load_dotenv

# Importa los modelos de Pydantic definidos en chatinterfases
from interfaces.chatinterfaces import ChatCompletionResponse, InputMessage # Asegurarse de importar ChatCompletionResponse si se usa como response_model

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa el router de FastAPI
router = APIRouter()

# --- Configuración del Cliente OpenAI para OpenRouter ---
# La API Key es crucial para la autenticación con OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    # Lanza un error si la API Key no está configurada, crucial para producción
    raise ValueError("La variable de entorno OPENROUTER_API_KEY no está configurada.")

# Inicializa el cliente de OpenAI apuntando a la base_url de OpenRouter
# Se recomienda un timeout para evitar que las peticiones se queden colgadas indefinidamente
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    timeout=60.0 # Define un timeout de 60 segundos para las solicitudes
)

# --- Ruta para la Interacción con el Modelo de IA ---
# Usamos response_model para que FastAPI valide y serialice la salida automáticamente
@router.post("/ai-chat", response_model=ChatCompletionResponse)
async def ai_chat(data: InputMessage):
    """
    Endpoint para procesar mensajes de usuario con el modelo de IA a través de OpenRouter.
    Recibe un mensaje de texto y devuelve la respuesta del modelo de IA.
    """
    try:
        user_message = data.message.strip()

        # Validación de entrada: El mensaje no puede estar vacío
        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El mensaje del usuario no puede estar vacío."
            )

        # Prompt del sistema para guiar el comportamiento del modelo
        system_prompt = (
            "Eres un asistente inteligente que responde en español de forma clara, "
            "concisa y amigable. Usa un lenguaje sencillo y apropiado para Colombia."
        )

        print(f"DEBUG: Mensaje de usuario recibido: '{user_message}'")

        # --- Llamada a la API de Completions de OpenRouter ---
        # **Corrección importante:** Se utiliza el modelo especificado originalmente.
        # Asegúrate de que este modelo esté disponible y sea el correcto para tu uso en OpenRouter.
        model_to_use = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free" # Corregido aquí

        completion = await client.chat.completions.create( # Usamos await para la llamada asíncrona
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        print(f"DEBUG: Respuesta cruda del modelo recibida: {completion.model_dump_json()}") # Para depuración

        # Validación de la respuesta del modelo
        if not completion or not completion.choices or not completion.choices[0].message.content:
            print("ERROR: La respuesta del modelo está vacía o incompleta.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="La respuesta del modelo de IA está vacía o no tiene el formato esperado."
            )

        # Extrae la respuesta del modelo
        # assistant_reply = completion.choices[0].message.content.strip() # Ya no es necesario extraer manualmente
        # print(f"DEBUG: Respuesta final del asistente: '{assistant_reply}'")

        # FastAPI serializará automáticamente este objeto Pydantic (completion) a JSON
        # Asegúrate de que tu modelo ChatCompletionResponse en chatinterfases.py
        # coincida con la estructura de 'completion'
        return completion

    # --- Manejo de Excepciones Específicas y Generales ---
    except OpenAIError as e:
        # Errores específicos de la librería OpenAI (problemas con la API key, formato de la petición, etc.)
        print(f"ERROR: Error de OpenAI al comunicarse con OpenRouter: {e}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY, # 502 Bad Gateway si el problema es con el servicio externo
            content={"reply": f"Error al comunicarse con el servicio de IA: {e.args[0] if e.args else 'Error desconocido de la API.'}"},
            media_type="application/json"
        )
    except httpx.TimeoutException:
        # Errores de timeout en la comunicación HTTP
        print("ERROR: Tiempo de espera agotado al comunicarse con OpenRouter.")
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, # 504 Gateway Timeout
            content={"reply": "El servicio de IA tardó demasiado en responder. Intenta de nuevo."},
            media_type="application/json"
        )
    except httpx.HTTPStatusError as e:
        # Errores HTTP generales (4xx, 5xx) que vienen de OpenRouter
        print(f"ERROR: Error HTTP de OpenRouter: {e.response.status_code} - {e.response.text}")
        return JSONResponse(
            status_code=e.response.status_code, # Retorna el código de estado original si es relevante
            content={"reply": f"Error del servicio de IA: {e.response.status_code} - {e.response.text}"},
            media_type="application/json"
        )
    except HTTPException as he:
        # Ya es una HTTPException, simplemente la re-lanzamos (FastAPI la capturará y la devolverá)
        raise he
    except Exception as e:
        # Captura cualquier otra excepción inesperada
        import traceback
        traceback.print_exc() # Para depuración: imprime la traza completa
        print(f"ERROR: Ocurrió un error inesperado: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"reply": "⚠️ Error interno del servidor. Por favor, intenta más tarde."},
            media_type="application/json"
        )
