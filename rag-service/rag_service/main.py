import asyncio
import os
import tempfile
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from langchain.memory import ConversationSummaryBufferMemory
from langchain_mongodb import MongoDBChatMessageHistory
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


load_dotenv()


logging.basicConfig(level=logging.DEBUG)


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)


class ChatResponse:
    response: str


@app.post("/chat")
async def chat(msg: ChatResponse) -> ChatResponse:
    chat_message_history = MongoDBChatMessageHistory(
        session_id="test_session",
        connection_string=os.getenv("MONGODB_CONNECTION_STRING")
    )
    memory = ConversationSummaryBufferMemory(
        llm=llm, chat_memory=chat_message_history,
    )


@app.delete("/chat/session/{session_id}")
async def delete_chat_session(session_id: str):
    chat_message_history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=os.getenv("MONGODB_CONNECTION_STRING")
    )
    chat_message_history.clear()

if __name__ == "__main__":
    #env get port
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
