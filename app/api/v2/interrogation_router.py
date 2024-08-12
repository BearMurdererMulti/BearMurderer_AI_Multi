from fastapi import APIRouter, Request, HTTPException

from app.services.game_service import GameService

router = APIRouter(
    prefix="/api/v2/interrogation",
    tags=["INTERROGATION"]
)
from pydantic import BaseModel

class NewInterRequest(BaseModel):
    gameNo: int
    npcName: str = "박동식"
    weapon: str | None = None

class NewInterResponse(BaseModel):
    message: str

class ConversationRequest(BaseModel):
    gameNo: int
    npcName: str = "박동식"
    content: str

class ConversationResponse(BaseModel):
    response: str
    heartRate: int

@router.post("/new", 
             description="새로운 취조를 시작하는 API 입니다.",
             response_model=NewInterResponse
            )
async def new_interrogation(request: Request, input: NewInterRequest):
    game_service: GameService = request.app.state.game_service
    game_service.new_interrogation(input.gameNo, input.npcName, input.weapon)

    return {"message": "New interrogation started"}

@router.post("/conversation", 
             description="취조에서 자유대화하는 API 입니다.",
             response_model=ConversationResponse
            )
async def interrogation(request: Request, input: ConversationRequest):
    game_service: GameService = request.app.state.game_service
    try:
        response = game_service.generation_interrogation_response(input.gameNo, input.npcName, input.content)
    except TypeError as e:
        raise HTTPException(status_code=404, detail=f"interrogation not found: {e}")
    return response