from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    max_tokens: int = 100
    temperature: float =0.7