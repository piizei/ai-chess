import os
import queue
import threading

import requests
from dotenv import load_dotenv
load_dotenv()
from game_service.model import VoteMessage
from game_service.vote_agent import get_move

votes = {}

stockfish = os.getenv("STOCKFISH_SERVER")

task_queue = queue.Queue()


def get_voted_move(turn: int, fen) -> str:
    if turn in votes:
        max_voted_move = max(votes[turn], key=votes[turn].get)
        return max_voted_move
    else:
        response = requests.post(stockfish + '/3', json={"fen": fen})
        return response.text.split(" ")[1]


def worker(global_games: dict):
    games = global_games
    while True:
        cmd: VoteMessage = task_queue.get()
        if cmd is None:
            break
        process_move(cmd, games["current_game"])
        task_queue.task_done()


def process_move(cmd: VoteMessage, game):
    if cmd.turn == len(game.moves):
        move = get_move(cmd.message, game.current_fen)
        if not cmd.turn in votes:
            votes[cmd.turn] = {f"{move.end + move.start}": 1}
        else:
            votes[cmd.turn][f"{move.end + move.start}"] += 1


