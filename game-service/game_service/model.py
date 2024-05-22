from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

games = {}


class VoteMessage(BaseModel):
    user: str
    message: str
    turn: int = 0


class VoteResponse(BaseModel):
    message: str
    is_ok: bool


class Move(BaseModel):
    start: str
    end: str


class Game(BaseModel):
    timestamp: datetime
    starts: datetime
    is_over: bool
    winner: Optional[str]
    moves: List[str]
    current_fen: str
    previous_fen: Optional[str]
    game_id: str
    last_move_at: Optional[datetime]
    last_move_described: Optional[str]
    turn_duration_seconds: int
    last_move: Optional[str]
    last_move_img: Optional[str]

