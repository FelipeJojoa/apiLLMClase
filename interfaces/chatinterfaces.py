from pydantic import BaseModel
from typing import List, Optional

class InputMessage(BaseModel):
    message: str
    model: Optional[str] = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    message: Message
    finish_reason: Optional[str] = None
    index: Optional[int] = 0

class ChatCompletionResponse(BaseModel):
    id: Optional[str]
    object: Optional[str]
    created: Optional[int]
    model: str
    choices: List[Choice]
    usage: Optional[Usage]