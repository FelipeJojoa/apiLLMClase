# llmTest.py
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

message = input("¿Cuál es tu pregunta?: ")

prompt = (
    "Por favor responde de manera clara y sin símbolos innecesarios. "
    "Evita usar otros idiomas que no sean el castellano y escribe una respuesta concisa. "
    f"Pregunta del usuario: {message}"
)

completion = client.chat.completions.create(
    model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("Respuesta del modelo:")
print(completion.choices[0].message.content)
