from fastapi import APIRouter
from openai import OpenAI

from interfaces.chatinterfaces import ChatCompletionResponse, InputMessage

router = APIRouter()

client = OpenAI(api_key="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",
                base_url="https://openrouter.ai/api/v1")

@router.post("/ai-chat")
def aiChat(data: InputMessage):
    data = data.model_dump()
    print("message: " + data["message"])

    message = "Por favor response de manera concreta, clara y siempre en castellano."

    try:
        completion: ChatCompletionResponse= client.chat.completions.create(
            model="google/gemma-3-1b-it:free",
            messages=[
                {
                    "role": "system",
                    "content":"Eres un asistente que siempre responde en castellano de forma clara y breve"
                },

                {
                    "role": "user", ""
                    "content":message + "responde a esta pregunta: " +data["message"]
                }
            ]
        )
        print("response: "+completion.choices[0].message.content)
        return {"response":completion.choices[0].message.content}
    except Exception as e:
        print(f"Error: {e}")
        return {"status":str(e)}

