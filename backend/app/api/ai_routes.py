from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.graph import graph
from app.core.security import get_current_user


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
    dependencies=[Depends(get_current_user)]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    result = graph.invoke(
        {
            "user_query": request.message,
            "tool_name": None,
            "tool_output": None,
            "final_response": None,
        }
    )

    return {
        "response": result["final_response"]
    }