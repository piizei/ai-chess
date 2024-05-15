import instructor

from game_service.model import Move
from game_service.openai_utils import get_openai

client = instructor.from_openai(get_openai())

system_message = """
Given a chessboard configuration in FEN notation and a natural language description of a move, output the start and end positions of the move in algebraic notation.

FEN Notation: {FEN}

User Move Description: {MOVE}

Interpret the FEN notation to understand the current board setup.
Analyze the user's move description to identify the piece and its intended move.
Translate the move into specific start and end positions using algebraic notation.

Output:
"""


def get_move(prompt: str, fen: str) -> Move:
    user_prompt = system_message.replace("{FEN}", fen).replace("{MOVE}", prompt)
    return client.chat.completions.create(
        model="gpt-4-turbo",
        response_model=Move,
        messages=[{"role": "user", "content": user_prompt}],
    )
