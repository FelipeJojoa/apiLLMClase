from fastapi import APIRouter
from interfaces.chatinterfaces import InputMessage
import os
from openai import OpenAI

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@router.post("/ai-chat")
def aiChat(data: InputMessage):
    data = data.model_dump()
    print("message: " + data["message"])
    print("model: " + data["model"])

    system_message = "Eres un asistente que siempre responde en castellano de forma clara y breve"
    user_prompt = "Por favor responde de manera concreta, clara y siempre en castellano. Responde a esta pregunta: " + data["message"]

    try:
        completion = client.chat.completions.create(
            model=data["model"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]
        )
        response = completion.choices[0].message.content
        print("response: " + response)
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": str(e)}
