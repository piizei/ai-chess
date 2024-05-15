from pydantic import BaseModel


class VoteMessage(BaseModel):
    user: str
    message: str


class VoteResponse(BaseModel):
    message: str
    is_ok: bool


class Move(BaseModel):
    start: str
    end: str
