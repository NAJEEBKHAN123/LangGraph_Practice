import sqlite3
import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY"),
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

# SQLite persistence
DB_PATH = os.path.join(os.path.dirname(__file__), "chatbot_memory.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=5000;")
checkpointer = SqliteSaver(conn)
checkpointer.setup()

graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def get_thread_history(thread_id: str):
    """Retrieve message history for a given thread_id."""
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    if not state or not state.values:
        return []
    return state.values.get("messages", [])

def get_all_threads():
    """Retrieve list of distinct threads with titles and message counts."""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
    rows = cursor.fetchall()
    threads_info = []
    
    for row in rows:
        tid = row[0]
        msgs = get_thread_history(tid)
        if msgs:
            title = "New Chat"
            for m in msgs:
                is_human = type(m).__name__ == "HumanMessage" or getattr(m, "type", "") == "human"
                if is_human:
                    content = m.content
                    if isinstance(content, list):
                        text = "".join(item.get("text", "") for item in content if isinstance(item, dict))
                        content = text or str(content)
                    title = str(content)[:35] + ("..." if len(str(content)) > 35 else "")
                    break
            threads_info.append({
                "id": tid,
                "title": title,
                "message_count": len(msgs)
            })
    return threads_info

def delete_thread(thread_id: str):
    """Delete all checkpoints and writes for a given thread_id."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
    cursor.execute("DELETE FROM writes WHERE thread_id = ?", (thread_id,))
    conn.commit()