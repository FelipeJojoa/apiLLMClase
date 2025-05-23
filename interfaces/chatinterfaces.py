from pydantic import BaseModel
from typing import List

# Modelo para la entrada del usuario al endpoint de chat
class InputMessage(BaseModel):
    message: str

# Modelos para la estructura de la respuesta de la API de OpenRouter (simulando OpenAI)
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

# Representa el contenido de un mensaje, típicamente con un rol y el texto
# Aunque el bot-message solo tiene content, es una buena práctica incluir role si el API lo devuelve
class Message(BaseModel):
    # role: str # Descomentar si el API de OpenRouter devuelve el rol del mensaje en choices
    content: str

# Representa una "elección" o una respuesta generada por el modelo
class Choices(BaseModel):
    # index: int # Descomentar si el API de OpenRouter devuelve el índice de la elección
    message: Message
    # finish_reason: str # Descomentar si el API de OpenRouter devuelve la razón de finalización

# Modelo completo para la respuesta de finalización de chat de la API
class ChatCompletionResponse(BaseModel):
    id: str # Añadido 'id' que OpenRouter/OpenAI suele devolver
    model: str
    choices: List[Choices]
    usage: Usage
    # created: int # Descomentar si el API de OpenRouter devuelve el timestamp de creación
    # object: str = "chat.completion" # Descomentar si el API de OpenRouter devuelve el tipo de objeto