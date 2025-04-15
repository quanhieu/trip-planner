from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

# Add to common/a2a_protocol.py:
class ContentNegotiation(BaseModel):
    supported_formats: list[str]
    preferred_format: str

class AgentCard(BaseModel):
    name: str
    description: str
    capabilities: list[str]
    api_version: str = "1.0"

class A2AMessage(BaseModel):
    message_id: str
    conversation_id: str
    content: Dict[str, Any]
    parent_message_id: Optional[str] = None
    role: str = "agent"

class A2AMessageType(str, Enum):
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"
    STATUS = "status"
    CAPABILITY = "capability"

class A2APayload(BaseModel):
    type: A2AMessageType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None