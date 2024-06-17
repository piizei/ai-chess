import asyncio
import os
import tempfile
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
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
    logging.info(f"Starting up {task}")
    logging.info(f"Starting up {worker_task}")
    yield
    logging.info("Shutting down")


app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

votes_per_user = {}


@app.post("/vote")
async def vote_move(msg: VoteMessage) -> VoteResponse:
    with tracer.start_as_current_span("vote") as span:
        turn = 0
        if get_game() is not None:
            turn = len(get_game().moves)
        if turn % 2 > 0:
            span.add_event("Invalid vote")
            return VoteResponse(is_ok=False, message="Please wait, It's AI's turn to move.")
        try:  # just ignore if there is concurrency issues
            if turn in votes_per_user:
                if msg.user in votes_per_user[turn]:
                    span.add_event("multiple vote")
                    return VoteResponse(is_ok=False, message="You have already voted for this turn.")
                else:
                    span.add_event("vote")
                    votes_per_user[turn].append(msg.user)
            else:
                votes_per_user[turn] = [msg.user]
        except Exception as e: # just ignore if there is concurrency issues
            span.add_event("Vote management crashed")
            logging.exception(f"An exception in vote management: {e}")

        msg.turn = turn
        await task_queue.put(msg)
        span.add_event("Queued vote")
        return VoteResponse(is_ok=True, message="Thank you, your vote has been registered.")


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
    #env get port
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
