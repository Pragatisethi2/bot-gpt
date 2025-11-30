from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CreateConversationRequest(BaseModel):
    user_id: int
    first_message: str
    mode: str = "chat"

class AddMessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

class ConversationResponse(BaseModel):
    id: int
    title: str
    mode: str
    created_at: datetime
    last_updated: datetime

class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]