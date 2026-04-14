import os

from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agent import APP

app = FastAPI(title="DevAssist")


class ChatRequest(BaseModel):
    model: str = "devassist-v1"
    messages: list[dict]
    session_id: str | None = None


class ChatResponse(BaseModel):
    choices: list[dict]
    usage: dict = {}


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

    user_content = req.messages[-1].get("content", "") if req.messages else ""

    thread_id = req.session_id or "default"
    config = {"configurable": {"thread_id": thread_id}}

    result = APP.invoke(
        {"messages": [HumanMessage(content=user_content)]},
        config=config,
    )

    last_message = result["messages"][-1]
    content = last_message.content if hasattr(last_message, "content") else str(last_message)

    return ChatResponse(
        choices=[{"message": {"role": "assistant", "content": content}, "finish_reason": "stop"}]
    )


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    return {"deleted": session_id, "note": "in-memory sessions persist until restart"}


@app.get("/health")
async def health():
    return {"status": "ok", "agent": "DevAssist", "model": os.getenv("MODEL", "gemini-2.0-flash")}
