from fastapi import APIRouter
from interfaces.chatinterfaces import InputMessage
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@router.post("/ai-chat")
async def ai_chat(data: InputMessage):
    try:
        user_input = data.message.strip()
        model_name = data.model.strip()

        if not user_input:
            return JSONResponse(status_code=400, content={"response": "El mensaje está vacío."})

        if not model_name:
            return JSONResponse(status_code=400, content={"response": "No se especificó el modelo."})

        system_prompt = "Eres un asistente que siempre responde en castellano de forma clara y breve."
        user_prompt = f"Por favor responde en castellano de forma clara y concisa: {user_input}"

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        content = completion.choices[0].message.content.strip()
        return JSONResponse(status_code=200, content={"response": content})

    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Error del servidor: {str(e)}"})
