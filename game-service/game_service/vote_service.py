import asyncio
import logging
import os
import traceback

import requests
from Chessnut import Game
from dotenv import load_dotenv

load_dotenv()
from game_service.model import VoteMessage
from game_service.vote_agent import get_move

votes = {}

stockfish = os.getenv("STOCKFISH_SERVER")

task_queue = asyncio.Queue()


def get_voted_move(turn: int, fen) -> str:
    logging.debug(f"Getting voted move for turn {turn}")
    if turn in votes:
        print(f"Votes: {votes[turn]}")
        max_voted_move = max(votes[turn], key=votes[turn].get)
        logging.debug(f"Most voted move in turn {turn} is {max_voted_move}")
        chess_game = Game(fen=fen)
        try:
            chess_game.apply_move(max_voted_move)
        except:
            logging.info(f"Invalid move {max_voted_move} for turn {turn}")
            # Invoke stockfish only to the depth of 3, so that the game ends eventually
            # (The AI is invoking to the default depth of 18)
            response = requests.post(stockfish + '/3', json={"fen": fen})
            return response.text.split(" ")[1]
        return max_voted_move
    else:
        response = requests.post(stockfish + '/3', json={"fen": fen})
        return response.text.split(" ")[1]


async def worker(global_games: dict):
    games = global_games
    while True:
        try:
            logging.debug("Waiting for votes")
            cmd: VoteMessage = await task_queue.get()
            if cmd is None:
                logging.debug("Received None, breaking the loop")
                break
            logging.debug(f"Processing vote: {cmd}")
            if games:
                process_move(cmd, games["current_game"])
            else:
                # Game has not started yet, use default-game
                process_move(cmd, Game())
            task_queue.task_done()
            logging.debug("Vote processed, waiting for the next one")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error(traceback.format_exc())


def process_move(cmd: VoteMessage, game):
    if cmd.turn == len(game.moves):
        move = get_move(cmd.message, game.current_fen)
        move_str = move.start + move.end
        if cmd.turn in votes:
            if move_str in votes[cmd.turn]:
                votes[cmd.turn][move_str] += 1
            else:
                votes[cmd.turn][move_str] = 1
        else:
            votes[cmd.turn] = {move_str: 1}

