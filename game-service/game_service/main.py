from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
import uvicorn

from game_service.model import VoteMessage, VoteResponse

load_dotenv()
app = FastAPI()


@app.post("/vote")
async def vote_move(msg: VoteMessage):
    return VoteResponse(message=f"Received vote from {msg.user} with message: {msg.message}", is_ok=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
