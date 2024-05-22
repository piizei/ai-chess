from dotenv import load_dotenv
load_dotenv()
from game_service.commentator_agent import comment_move
from game_service.vote_agent import get_move


def test_input():
    move = get_move("move left knight forward left",
                    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert move.start == "b1"
    assert move.end == "a3"


def test_commentator():
    comment = comment_move("4qr2/p1r3k1/b2p1p1p/2pP2p1/Pp2P3/1P2R2P/3N1PPK/3QR3 b - - 47 101", "AI", "c2d1")
    assert comment=="abc"
