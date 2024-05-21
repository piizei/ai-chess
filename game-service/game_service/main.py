import asyncio
import tempfile
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

load_dotenv()
from game_service.game_state import game_loop, get_game
from game_service.model import VoteMessage, VoteResponse

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
async def vote_move(msg: VoteMessage):
    return VoteResponse(message=f"Received vote from {msg.user} with message: {msg.message}", is_ok=True)


@app.get("/status")
async def status():
    game = get_game()
    if game:
        return game.dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
