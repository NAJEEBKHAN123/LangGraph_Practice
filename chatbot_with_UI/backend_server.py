from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langgraph_backend import chatbot, get_all_threads, get_thread_history, delete_thread
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

app = FastAPI(title="LangGraph Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    thread_id: str = "default"

class ChatResponse(BaseModel):
    role: str
    content: str

class ThreadItem(BaseModel):
    id: str
    title: str
    message_count: int

from fastapi.responses import StreamingResponse
import json

@app.post("/api/chat")
def chat(request: ChatRequest):
    user_message = request.messages[-1].content if request.messages else ""
    config = {"configurable": {"thread_id": request.thread_id}}

    def stream_generator():
        try:
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_message)]},
                config=config,
                stream_mode="messages"
            ):
                content = message_chunk.content
                if isinstance(content, list):
                    text = "".join(item.get("text", "") for item in content if isinstance(item, dict))
                    content = text
                elif not isinstance(content, str):
                    content = str(content) if content else ""
                
                if content:
                    payload = json.dumps({"content": content})
                    yield f"data: {payload}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as ai_error:
            print(f"Streaming error: {ai_error}")
            fallback = get_fallback_response(user_message)
            payload = json.dumps({"content": fallback})
            yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

@app.get("/api/threads", response_model=List[ThreadItem])
def list_threads():
    try:
        return get_all_threads()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{thread_id}")
def fetch_history(thread_id: str):
    try:
        messages = get_thread_history(thread_id)
        result = []
        for m in messages:
            role = "user" if (type(m).__name__ == "HumanMessage" or getattr(m, "type", "") == "human") else "assistant"
            content = m.content
            if isinstance(content, list):
                text_content = "".join(item.get("text", "") for item in content if isinstance(item, dict))
                content = text_content or str(content)
            elif not isinstance(content, str):
                content = str(content)
            result.append({"role": role, "content": content})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/threads/{thread_id}")
def remove_thread(thread_id: str):
    try:
        delete_thread(thread_id)
        return {"status": "deleted", "thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_fallback_response(user_message: str) -> str:
    """Generate a simple fallback response when AI is unavailable"""
    responses = [
        f"I received your message: '{user_message}'. The AI backend encountered an error. Please verify your configuration.",
        f"You said: '{user_message}'. I'm currently running in fallback mode.",
    ]
    import random
    return random.choice(responses)

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)