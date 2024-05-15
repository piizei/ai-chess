from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
from game_service.game_state import create_game, check_game


def test_start():
    create_game(datetime.now())
    state = check_game()
    print(state)
