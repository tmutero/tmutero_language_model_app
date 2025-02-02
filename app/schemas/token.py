from pydantic import BaseModel
from typing import Any, List, Optional, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
