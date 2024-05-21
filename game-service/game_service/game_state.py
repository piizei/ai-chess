import asyncio
import secrets
from datetime import datetime

import requests
from fentoboardimage import fenToImage, loadPiecesFolder

from game_service.model import Game
from game_service.mongo_utils import get_collection

base_url = "http://localhost:3000/api/v1/chess/two"
stockfish = "http://localhost:8080/"

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
        game_id="",
        last_move_at=datetime.now(),
        last_move_described=None,
        turn_duration_seconds=20,
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


games = {}


def get_game():
    return games["current_game"]


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
                    # check if white moves
                    if is_fen_white(game):
                        # change to black turn
                        print("White moves")
                        response = requests.post(stockfish, json={"fen": game.current_fen})
                        move = response.text.split(" ")[1]
                        (start, end) = move[:2], move[2:]
                        print(move)
                        game.last_move_described = f"White moves {start} to {end}"
                        await update_turn(static_dir, game, start, end)
                    else:
                        print("Black moves")
                        response = requests.post(stockfish, json={"fen": game.current_fen})
                        move = response.text.split(" ")[1]
                        (start, end) = move[:2], move[2:]
                        print(move)
                        game.last_move_described = f"Black moves {start} to {end}"
                        await update_turn(static_dir, game, start, end)
            else:
                print("No game found")

            await asyncio.sleep(loop_interval)
        except Exception as e:
            print(games["current_game"])
            print(f"An error occurred in game_loop: {e}")
            await asyncio.sleep(loop_interval)


async def update_turn(static_dir, game, start, end):
    print("Making move")
    requests.post(f"{base_url}/move", json={"game_id": game.game_id, "from": start, "to": end})
    print("Checking game")
    response = requests.post(f"{base_url}/check", json={"game_id": game.game_id})
    game.is_over = response.json()["status"] != "game continues"
    if game.is_over:
        game.winner = response.json()["status"]
    print("Checking")
    response = requests.post(f"{base_url}/fen", json={"game_id": game.game_id})
    print(response.json())
    game.current_fen = response.json()["fen_string"]
    print("Creating image")
    image = fenToImage(
        fen=game.current_fen,
        squarelength=30,
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
