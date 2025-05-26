from fastapi import APIRouter
from openai import OpenAI
from interfaces.chatinterfaces import ChatCompletionResponse, InputMessage

router = APIRouter()

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

@router.post("/ai-chat")
def ai_chat(data: InputMessage):
    try:
        prompt = (
            "Por favor responde de manera concreta, clara y siempre en castellano. "
            f"Responde a esta pregunta: {data.message}"
        )

        completion: ChatCompletionResponse = client.chat.completions.create(
            model=data.model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente útil que responde siempre en castellano de forma clara y concisa."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = completion.choices[0].message.content
        return {"response": response_text}

    except Exception as e:
        return {"error": str(e)}
