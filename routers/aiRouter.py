from fastapi import APIRouter
from interfaces.chatinterfaces import InputMessage
import os
from openai import OpenAI

router = APIRouter()

# Cliente de OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@router.post("/ai-chat")
def ai_chat(data: InputMessage):
    try:
        user_input = data.message.strip()
        model_name = data.model.strip()

        if not user_input:
            return {"response": "El mensaje está vacío."}

        if not model_name:
            return {"response": "No se especificó el modelo."}

        system_prompt = "Eres un asistente que siempre responde en castellano de forma clara y breve."
        full_prompt = f"Por favor responde en castellano a la siguiente pregunta: {user_input}"

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ]
        )

        if not completion or not completion.choices:
            return {"response": "No se recibió respuesta del modelo."}

        content = completion.choices[0].message.content
        return {"response": content}

    except Exception as e:
        # Capturamos todos los errores como respuesta JSON válida
        return {"response": f"Error al procesar la solicitud: {str(e)}"}
