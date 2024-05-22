import asyncio
import tempfile
import threading
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles
load_dotenv()
from game_service.vote_service import task_queue, worker
from game_service.game_state import game_loop, get_game
from game_service.model import VoteMessage, VoteResponse, games

# Tmp for Static files directory
tmp_dir = tempfile.TemporaryDirectory()
static_dir = tmp_dir.name


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(game_loop(static_dir))
    print(f"Starting up {task}")
    yield
    print("Shutting down")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.post("/vote")
async def vote_move(msg: VoteMessage)-> VoteResponse:
    task_queue.put(msg)
    return VoteResponse(is_ok=True, message="Thank you, Your vote has been registered.")


@app.get("/status")
async def status():
    game = get_game()
    if game:
        return game.dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    worker_thread = threading.Thread(target=worker, args=(games,), daemon=True)
    worker_thread.start()
