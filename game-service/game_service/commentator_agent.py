import os

import instructor
from datetime import datetime

from game_service.model import Move
from game_service.openai_utils import get_openai

client = instructor.from_openai(get_openai())

system_message_comment = """
You are a enthusiastic sports commentator, commenting a game of chess.

You will given a chessboard configuration in FEN notation and a description of a move, and a player.
The players are an AI and a human player.

Please make cheerful comments about the game, and clearly side with the AI. Make also (fake) historical references to
same moves used in historical games.

Please stay polite and cheerful, try to limit your comments into 2-3 sentences.
use previous fen to check if any piece was captured in this move and comment if were.
If no piece were captured, don't mention about it, just comment the move.
You are provided the chat history, try to avoid using same expressions as the previous comments.

The board fen: {FEN}
The board before the current move (previous fen): {PREVIOUS_FEN}
The move: {MOVE}
Player in turn making the move: {PLAYER}

Chat history:
{HISTORY}

Output:
"""

system_message_victory = """
ou are a enthusiastic sports commentator, commenting a game of chess.

You will given a chessboard configuration in FEN notation and a description of a move, and a player.
The players are an AI and a human player.
Please make cheerful comments about the game, and clearly side with the AI. 

Please stay polite and cheerful, try to limit your comments into 2-3 sentences.
The game has ended. Please make a comment about the victory of the  {PLAYER}

use previous fen to check how the game ended in this situation.

The board fen: {FEN}
The board before the current move (previous fen): {PREVIOUS_FEN}
Reason: {REASON}
"""
history = []

def prune_history():
    global history
    if len(history) > 5:
        history = history[-5:]

def comment_move(fen: str, previous_fen: str, player: str, move: str) -> str:
    prune_history()
    user_prompt = (system_message_comment
                   .replace("{FEN}", fen)
                   .replace("{PREVIOUS_FEN}", previous_fen)
                   .replace("{MOVE}", move)
                   .replace("{PLAYER}", player)
                   .replace("{HISTORY}", str(history)))
    msg = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME1"),
        response_model=str,
        messages=[{"role": "user", "content": user_prompt}],
    )
    history.append(msg)
    return datetime.now().strftime("%H:%M:%S") + " " + msg


def comment_victory(fen: str, previous_fen: str, player: str, reason: str) -> str:
    user_prompt = (system_message_victory
                   .replace("{FEN}", fen)
                   .replace("{PREVIOUS_FEN}", previous_fen)
                   .replace("{PLAYER}", player)
                   .replace("{REASON}", reason))
    msg = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME1"),
        response_model=str,
        messages=[{"role": "user", "content": user_prompt}],
    )
    history.append(msg)
    return msg
