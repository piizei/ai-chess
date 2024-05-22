import asyncio
import os
import secrets
from datetime import datetime

import requests
from fentoboardimage import fenToImage, loadPiecesFolder

from game_service.commentator_agent import comment_move, comment_victory
from game_service.model import Game, games
from game_service.mongo_utils import get_collection
from game_service.vote_service import get_voted_move

base_url = os.getenv("CHESS_API")
stockfish = os.getenv("STOCKFISH_SERVER")

loop_interval = 5


def create_game(start_date: datetime):
    collection = get_collection()
    game = Game(
        timestamp=datetime.now(),
        starts=datetime.now(),
        is_over=False,
        winner=None,
        moves=[],
        current_fen="",
        previous_fen=None,
        game_id="",
        last_move_at=datetime.now(),
        last_move_described=None,
        turn_duration_seconds=60,
        last_move=None,
        last_move_img=None,
    )
    response = requests.get(f"{base_url}")
    game.game_id = response.json()["game_id"]
    response = requests.post(f"{base_url}/fen", json={"game_id": game.game_id})
    game.current_fen = response.json()["fen_string"]
    result = collection.insert_one(game.dict())


def check_game():
    #find games that are started (start date is before datetime.now( and  are not over and have no game_id
    return get_collection().find_one({"starts": {"$lt": datetime.now()}, "is_over": False})


def update_game(game: Game):
    get_collection().update_one({"game_id": game.game_id}, {"$set": game.dict()})


def is_fen_white(game: Game):
    if game.current_fen:
        return "w" in game.current_fen
    return False



def get_turn() -> int:
    if "current_game" in games:
        return len(games["current_game"].moves)
    else:
        return 0


def get_game():
    if "current_game" in games:
        return games["current_game"]
    else:
        return None


def get_previous_game():
    return games["previous_game"]


async def game_loop(static_dir: str):
    game = None
    while True:
        try:
            print("Running task")
            if "current_game" not in games or games["current_game"].is_over:
                game_dict = check_game()
                if game_dict:
                    game = Game(**game_dict)
                    games["current_game"] = game
            else:
                game = games["current_game"]

            if game and not game.is_over:
                print("game running")
                # check if turn_duration_seconds has passed since last move
                if (datetime.now() - game.last_move_at).seconds > game.turn_duration_seconds:
                    print("Time has passed")
                    move = get_voted_move(len(game.moves), game.current_fen)
                    # check if white moves
                    if is_fen_white(game):
                        print("Humans move")
                        await update_turn(static_dir, game, move, "human")
                    else:
                        print("AI moves")
                        await update_turn(static_dir, game, move, "AI")
            else:
                print("No game found")

            await asyncio.sleep(loop_interval)
        except Exception as e:
            print(games["current_game"])
            print(f"An error occurred in game_loop: {e}")
            await asyncio.sleep(loop_interval)


async def update_turn(static_dir, game, move, player):
    print(f"Making move {move}")
    (start, end) = move[:2], move[2:]
    requests.post(f"{base_url}/move", json={"game_id": game.game_id, "from": start, "to": end})
    print("Checking game")
    response = requests.post(f"{base_url}/check", json={"game_id": game.game_id})
    game.is_over = response.json()["status"] != "game continues"
    game.previous_fen = game.current_fen
    response = requests.post(f"{base_url}/fen", json={"game_id": game.game_id})
    game.current_fen = response.json()["fen_string"]
    if game.is_over:
        game.winner = response.json()["status"]
        game.last_move_described = comment_victory(game.current_fen, game.previous_fen, player, game.winner)
    else:
        game.last_move_described = comment_move(game.current_fen, game.previous_fen, player, start+end)
    print("Creating image")
    image = fenToImage(
        fen=game.current_fen,
        squarelength=33,
        darkColor="#D18B47",
        lightColor="#FFCE9E",
        pieceSet=loadPiecesFolder("./pieces"),
        lastMove={"before": start, "after": end, "darkColor": "#1D9413", "lightColor": "#32F321"},
    )
    random_name = secrets.token_hex(8)
    image.save(f"{static_dir}/{random_name}.png")
    game.last_move_img = f"{random_name}.png"
    game.last_move_at = datetime.now()
    game.moves.append(start + end)
    game.timestamp = datetime.now()
    update_game(game)
