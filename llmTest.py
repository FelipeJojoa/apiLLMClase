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