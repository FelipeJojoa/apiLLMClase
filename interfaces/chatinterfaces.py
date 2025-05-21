from pydantic import BaseModel

class InputMessage(BaseModel):
    message: str
    model: str

class Usage (BaseModel):
    prompt_tockens: int
    completion_tockens: int
    total_tockens: int

class Message(BaseModel):
    content: str

class Choices(BaseModel):
    message: Message

class ChatCompletionResponse (BaseModel):
    model: str
    choises: list[Choices]
    usage: Usage