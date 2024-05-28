from dotenv import load_dotenv
load_dotenv()
from game_service.commentator_agent import comment_move
from game_service.vote_agent import get_move


def test_input():
    move = get_move("move left knight forward left",
                    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert move.start == "b1"
    assert move.end == "a3"
    move = get_move("g2 to g3",
                    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert move.start == "g2"
    assert move.end == "g3"


