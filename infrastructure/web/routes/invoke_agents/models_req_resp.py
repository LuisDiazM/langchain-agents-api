from pydantic import BaseModel


class AgentRequest(BaseModel):
    session_id: str
    content: str

class ChatbotResponse(BaseModel):
    response: str
    session_id: str