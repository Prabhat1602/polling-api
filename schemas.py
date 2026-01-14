from pydantic import BaseModel
from typing import List

class PollCreate(BaseModel):
    question: str
    options: List[str]

class VoteCreate(BaseModel):
    user_id: str
    option_id: int
