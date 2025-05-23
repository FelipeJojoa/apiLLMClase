from openai import OpenAI

client = OpenAI(

    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

user_input = input("¿Cuál es tu pregunta?: ")

prompt = (
    "Por favor responde de manera clara y sin símbolos innecesarios. "
    "Evita usar otros idiomas que no sean castellano y escribe una respuesta concisa. "
    f"Pregunta del usuario: {user_input}"
)

completion = client.chat.completions.create(
    model="google/gemma-3-1b-it:free",
    messages=[{"role": "user", "content": prompt}]
)

print("🔍 Respuesta del modelo:")
print(completion.choices[0].message.content.strip())
