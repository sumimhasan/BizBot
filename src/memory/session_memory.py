# src/memory/session_memory.py
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict, Optional

# In-memory store (replace with Redis/DynamoDB in production)
SESSION_STORE: Dict[str, BaseChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create chat history for a session."""
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = ChatMessageHistory()
    return SESSION_STORE[session_id]

def clear_session_history(session_id: str) -> None:
    """Clear chat history for a session."""
    if session_id in SESSION_STORE:
        SESSION_STORE[session_id].clear()

def get_session_history_window(session_id: str, window_size: int = 5):
    """Get last N messages from session history."""
    history = get_session_history(session_id)
    return history.messages[-window_size:]