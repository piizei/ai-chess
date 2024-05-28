import asyncio
import tempfile
import threading
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

from game_service.telemetry import tracer

load_dotenv()
from game_service.vote_service import task_queue, worker
from game_service.game_state import game_loop, get_game, get_next_game
from game_service.model import VoteMessage, VoteResponse, games, Game

# Tmp for Static files directory
tmp_dir = tempfile.TemporaryDirectory()
static_dir = tmp_dir.name
logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(game_loop(static_dir))
    worker_task = asyncio.create_task(worker(games))
    print(f"Starting up {task}")
    print(f"Starting up {worker_task}")
    yield
    print("Shutting down")


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.post("/vote")
async def vote_move(msg: VoteMessage) -> VoteResponse:
    with tracer.start_as_current_span("vote") as span:
        turn = 0
        if get_game() is not None:
            turn = len(get_game().moves)
        msg.turn = turn
        await task_queue.put(msg)
        span.add_event("Queued vote")
        return VoteResponse(is_ok=True, message="Thank you, Your vote has been registered.")


@app.get("/status")
async def status():
    game = get_game()
    if game:
        return game.dict()
    else:
        next_game = get_next_game()
        if next_game:
            return Game(**next_game)
        else:
            return {"status": "No game found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
