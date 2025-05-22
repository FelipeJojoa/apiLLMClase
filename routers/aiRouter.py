from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from interfaces.chatinterfaces import InputMessage
import os
from openai import OpenAI

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@router.post("/ai-chat")
async def ai_chat(data: InputMessage):
    try:
        user_message = data.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

        prompt = "Por favor responde de manera concreta, clara y siempre en castellano."

        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente inteligente que responde en español (Colombia), de forma clara, "
                        "concisa y siempre manteniendo un tono respetuoso y amigable. Responde de manera precisa a las "
                        "preguntas del usuario, usando un lenguaje sencillo, directo y adaptado al contexto colombiano."
                    ),
                },
                {
                    "role": "user",
                    "content": f"{prompt} Responde a esta pregunta: {user_message}",
                },
            ],
        )

        if not completion or not completion.choices or not completion.choices[0].message.content:
            raise ValueError("La respuesta del modelo está vacía o mal formada.")

        respuesta = completion.choices[0].message.content.strip()
        print("✅ Respuesta del modelo:", respuesta)

        return JSONResponse(content={"reply": respuesta}, media_type="application/json")

    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"reply": "⚠️ Error interno del servidor. Intenta más tarde."},
            media_type="application/json"
        )

