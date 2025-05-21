from fastapi import APIRouter
from interfaces.chatinterfaces import InputMessage
import os
from openai import OpenAI

router = APIRouter()

# Configuración del cliente de OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@router.post("/ai-chat")
def ai_chat(data: InputMessage):
    data = data.model_dump()
    print(f"Mensaje recibido: {data['message']}")
    print(f"Modelo seleccionado: {data['model']}")

    system_message = "Eres un asistente que siempre responde en castellano de forma clara y breve."
    user_prompt = (
        "Por favor responde de manera concreta, clara y siempre en castellano. "
        f"Responde a esta pregunta: {data['message']}"
    )

    try:
        completion = client.chat.completions.create(
            model=data["model"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]
        )

        if completion and completion.choices:
            response = completion.choices[0].message.content
            print(f"Respuesta del modelo: {response}")
            return {"response": response}
        else:
            return {"response": "No se obtuvo una respuesta del modelo."}

    except Exception as e:
        print(f"Error en la solicitud: {e}")
        return {"response": f"Error del servidor: {str(e)}"}
