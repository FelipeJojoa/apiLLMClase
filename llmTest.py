import os
from openai import OpenAI, OpenAIError # Importa OpenAIError para un manejo más específico
from dotenv import load_dotenv # Importa load_dotenv para cargar variables de entorno
import sys # Para salir del script en caso de error crítico

# --- Carga de Variables de Entorno ---
# Carga las variables de entorno desde un archivo .env
load_dotenv()

# --- Configuración del Cliente OpenAI para OpenRouter ---
# Obtener la API Key desde las variables de entorno (¡NO hardcodeada!)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("ERROR: La variable de entorno OPENROUTER_API_KEY no está configurada.", file=sys.stderr)
    print("Por favor, asegúrate de tener un archivo .env con OPENROUTER_API_KEY='tu_key_aqui'.", file=sys.stderr)
    sys.exit(1) # Salir del script si la clave no está presente

client = OpenAI(
    api_key=OPENROUTER_API_KEY, # Usa la API Key de la variable de entorno
    base_url="https://openrouter.ai/api/v1",
    timeout=60.0 # Añade un timeout para evitar que las peticiones se queden colgadas
)

# --- Definición del Modelo de IA ---
# **Corrección importante:** Se utiliza el modelo especificado en la descripción.
MODEL_TO_USE = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"

# --- Interacción con el Usuario ---
user_input = input("✨ ¡Hola! ¿Cuál es tu pregunta para Dolphin 3.0 Mistral?: ")

if not user_input.strip():
    print("El mensaje no puede estar vacío. Por favor, ingresa una pregunta válida.")
    sys.exit(0) # Salir amigablemente si el usuario no ingresa nada

# --- Construcción del Prompt para el Modelo ---
# Se utiliza un prompt de sistema para dar contexto al modelo, similar a aiRouter.py
system_prompt = (
    "Eres un asistente inteligente que responde en español de forma clara, "
    "concisa y amigable. Usa un lenguaje sencillo y apropiado para Colombia."
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input.strip()}
]

# --- Llamada a la API de Completions y Manejo de Errores ---
try:
    print(f"\n🚀 Enviando tu pregunta al modelo {MODEL_TO_USE}...")
    completion = client.chat.completions.create(
        model=MODEL_TO_USE,
        messages=messages
    )

    # --- Procesamiento y Visualización de la Respuesta ---
    if completion and completion.choices and completion.choices[0].message.content:
        response_content = completion.choices[0].message.content.strip()
        print("\n🐬 Respuesta del modelo Dolphin:")
        print("------------------------------")
        print(response_content)
        print("------------------------------")
        if completion.usage:
            print(f"\n📊 Uso de tokens: Prompt={completion.usage.prompt_tokens}, Completion={completion.usage.completion_tokens}, Total={completion.usage.total_tokens}")
    else:
        print("\n⚠️ El modelo no proporcionó una respuesta válida o la respuesta está vacía.")

except OpenAIError as e:
    # Captura errores específicos de la librería OpenAI (problemas de autenticación, límite de tokens, etc.)
    print(f"\n❌ Error al comunicarse con OpenRouter: {e}", file=sys.stderr)
    print("Verifica tu API Key y el estado del servicio de OpenRouter.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    # Captura cualquier otra excepción inesperada
    print(f"\n❌ Ocurrió un error inesperado: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc() # Imprime la traza completa para depuración
    sys.exit(1)
