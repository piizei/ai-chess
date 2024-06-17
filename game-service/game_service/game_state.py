import asyncio
import os
import secrets
from datetime import datetime
import logging
import requests
from fentoboardimage import fenToImage, loadPiecesFolder
from opentelemetry.trace import StatusCode, Status
from cachetools import TTLCache, cached
from game_service.commentator_agent import comment_move, comment_victory
from game_service.model import Game, games
from game_service.mongo_utils import get_collection
from game_service.telemetry import tracer
from game_service.vote_service import get_voted_move

base_url = os.getenv("CHESS_API")
stockfish = os.getenv("STOCKFISH_SERVER")

loop_interval = 10
minimum_wait = 15


def create_game(start_date: datetime):
    collection = get_collection()
    game = Game(
        timestamp=datetime.now(),
        starts=start_date,
        is_over=False,
        winner=None,
        moves=[],
        current_fen="",
        previous_fen=None,
        game_id="",
        last_move_at=start_date,
        last_move_described=None,
        turn_duration_seconds=180,
        last_move=None,
        last_move_img=None,
    )
    response = requests.get(f"{base_url}")
    resp_json = response.json()
    if "game_id" in resp_json:
        game.game_id = response.json()["game_id"]
        response = requests.post(f"{base_url}/fen", json={"game_id": game.game_id})
        game.current_fen = response.json()["fen_string"]
        return collection.insert_one(game.dict())
    else:
        logging.error("No game_id in response")
        print(resp_json)
        print(response)
        return None


@cached(cache=TTLCache(maxsize=32, ttl=30))
def check_game():
    return get_collection().find_one({"starts": {"$lt": datetime.now()}, "is_over": False})


@cached(cache=TTLCache(maxsize=32, ttl=30))
def get_next_game():
    return get_collection().find_one({"starts": {"$gt": datetime.now()}, "is_over": False})


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


def get_best_move(fen: str) -> str:
    response = requests.post(stockfish, json={"fen": fen})
    return response.text.split(" ")[1]


async def game_loop(static_dir: str):
    game = None
    while True:
        with tracer.start_as_current_span("game-loop") as span:
            try:
                logging.debug("Running task")
                if "current_game" not in games or games["current_game"].is_over:
                    game_dict = check_game()
                    if game_dict:
                        logging.debug("Loaded game")
                        span.add_event("Loaded game")
                        game = Game(**game_dict)
                        games["current_game"] = game
                    else:
                        logging.debug("No game found in database")
                        span.add_event("No game found from database")
                else:
                    game = games["current_game"]

                if game and not game.is_over:
                    span.add_event("Running existing game")
                    is_human_turn = is_fen_white(game)
                    wait_time = game.turn_duration_seconds if is_human_turn else minimum_wait
                    # check if turn_duration_seconds has passed since last move
                    if (datetime.now() - game.last_move_at).seconds > wait_time:
                        logging.debug("Time has passed")
                        # check if white moves
                        if is_fen_white(game):
                            logging.info("Humans move")
                            move = get_voted_move(len(game.moves), game.current_fen)
                            await update_turn(static_dir, game, move, "human")
                        else:
                            logging.info("AI moves")
                            move = get_best_move(game.current_fen)
                            await update_turn(static_dir, game, move, "AI")
                else:
                    logging.debug("No game found")
                    span.add_event("No game found")
                await asyncio.sleep(loop_interval)
            except Exception as e:
                span.add_event("Exception in game loop")
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                logging.exception(f"An error occurred in game_loop: {e}")
                logging.debug(games["current_game"])
                logging.error(f"An error occurred in game_loop: {e}")
                await asyncio.sleep(loop_interval)


async def update_turn(static_dir, game, move, player):
    logging.debug(f"Making move {move}")
    (start, end) = move[:2], move[2:]
    with requests.post(f"{base_url}/move", json={"game_id": game.game_id, "from": start, "to": end}) as response:
        response.raise_for_status()
    logging.debug("Checking game")
    with requests.post(f"{base_url}/check", json={"game_id": game.game_id}) as check_response:
        check_response.raise_for_status()
        game.is_over = check_response.json()["status"] != "game continues"
    game.previous_fen = game.current_fen
    with requests.post(f"{base_url}/fen", json={"game_id": game.game_id}) as response:
        response.raise_for_status()
        response_json = response.json()
        if "fen_string" in response_json:
            game.current_fen = response_json["fen_string"]
        else:
            logging.error("No fen_string in response")
            # Todo, likely the game had expired. Figure out recovery.
    if game.is_over:
        game.winner = check_response.json()["status"]
        game.last_move_described = comment_victory(game.current_fen, game.previous_fen, player, game.winner)
    else:
        game.last_move_described = "Turn " + str(len(game.moves)) + " " + comment_move(game.current_fen,
                                                                                       game.previous_fen,
                                                                                       player,
                                                                                       start + end)
    logging.debug("Creating image")
    # are we running in docker:
    path = os.getcwd()
    if "/usr/src/app" in path:
        path = "/usr/src/app/pieces"
    else:
        path = "./pieces"

    image = fenToImage(
        fen=game.current_fen,
        squarelength=33,
        darkColor="#D18B47",
        lightColor="#FFCE9E",
        pieceSet=loadPiecesFolder(path),
        lastMove={"before": start, "after": end, "darkColor": "#1D9413", "lightColor": "#32F321"},
    )
    random_name = secrets.token_hex(8)
    image.save(os.path.join(static_dir, f"{random_name}.png"))
    game.last_move_img = f"{random_name}.png"
    game.last_move_at = datetime.now()
    game.moves.append(move)
    game.timestamp = datetime.now()
    update_game(game)
