from openai import OpenAI

client = OpenAI(api_key="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",
                base_url="https://openrouter.ai/api/v1")

messages = input("Cual es tu pregunta: ")

prompt = (
    "Por favor responde de manera clara y sin simbolos innecesarios"
    "Evita usar otros idiomas que no sean el castellano y escribe una respuesta concisa"
    f"Pregunta del usaurio: {messages}"
)

completion = client.chat.completions.create(
    model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
    messages=[
        {
            "role": "user",
            "content":prompt   
        }
    ]
)

print(completion.choices[0].message.content)
