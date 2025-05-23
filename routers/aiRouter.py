from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from interfaces.chatinterfaces import InputMessage
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/ai-chat")
async def ai_chat(data: InputMessage):
    user_message = data.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "cognitivecomputations/dolphin-2.5-mixtral-8x7b:free",
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente inteligente que responde en español de forma clara, concisa y amigable. Usa un lenguaje sencillo y adaptado a Colombia."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            raise ValueError("Respuesta del servidor no es JSON. Recibido: " + content_type)

        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()

        return JSONResponse(content={"reply": reply})

    except requests.exceptions.RequestException as e:
        print("❌ Error de red o autenticación:", str(e))
        raise HTTPException(status_code=502, detail="Error al contactar OpenRouter")
    except Exception as e:
        print("❌ Error inesperado:", str(e))
        return JSONResponse(
            status_code=500,
            content={"reply": "⚠️ Error interno del servidor. Intenta más tarde."},
        )

