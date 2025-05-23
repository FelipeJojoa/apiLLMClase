from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from interfaces.chatinterfaces import InputMessage
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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

        system_prompt = (
            "Eres un asistente inteligente que responde en español de forma clara, "
            "concisa y amigable. Usa un lenguaje sencillo y apropiado para Colombia."
        )

        completion = client.chat.completions.create(
            model="google/gemma-3-1b-it:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        if not completion or not completion.choices:
            raise ValueError("La respuesta del modelo está vacía.")

        respuesta = completion.choices[0].message.content.strip()
        print("Respuesta del modelo:", respuesta)
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
