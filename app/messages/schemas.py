from typing import Optional, Dict, Any

from pydantic import BaseModel

class MessagesCreate(BaseModel):
    message_id: int
    from_user_id: int
    chat_id: int
    text: str
    date: int
