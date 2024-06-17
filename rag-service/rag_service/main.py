import os
import logging
from typing import Optional

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import uvicorn
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_mongodb import MongoDBChatMessageHistory
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

from rag_service.ai_retriever import AISearchRetriever
from rag_service.config import config
from rag_service.openai_helper import get_llm
from rag_service.prompts import CUSTOM_CHATBOT_PREFIX

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

class ChatRequest(BaseModel):
    prompt: str
    user: str
    session: str

class ChatResponse(BaseModel):
    type: str = "chat_response"
    answer: Optional[str]



@app.post("/chat")
async def chat(msg: ChatRequest) -> ChatResponse:
    retriever = AISearchRetriever(indexes=config["AZURE_SEARCH_INDEX"].split(","))
    chat_message_history = MongoDBChatMessageHistory(
        session_id=msg.session,
        connection_string=config["MONGO_CONNECTION"]
    )
    llm = get_llm(max_tokens=config["LLM_MAX_TOKENS"], verbose=True)
    memory = ConversationSummaryBufferMemory(
        llm=llm, chat_memory=chat_message_history, output_key="answer", memory_key="chat_history", return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever,
                                                  memory=memory)
    chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate.from_template(
        CUSTOM_CHATBOT_PREFIX)
    answer = await chain.ainvoke({"question": msg.prompt})
    print(answer)
    return ChatResponse(answer=answer['answer'])


@app.delete("/chat/session/{session_id}")
async def delete_chat_session(session_id: str):
    chat_message_history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=os.getenv("MONGO_CONNECTION")
    )
    chat_message_history.clear()


if __name__ == "__main__":
    #env get port
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
