from fastapi import APIRouter, Request

from app.services.game_service import GameService

router = APIRouter(
    prefix="/api/v2/interrogation",
    tags=["INTERROGATION"]
)
from pydantic import BaseModel

class NewInterRequest(BaseModel):
    gameNo: int
    npc_name: str = "박동식"
    weapon: str = "독약"

class ConversationRequest(BaseModel):
    gameNo: int
    npc_name: str = "박동식"
    content: str

@router.post("/new", 
            )
async def new_interrogation(request: Request, input: NewInterRequest):
    game_service: GameService = request.app.state.game_service
    game_service.new_interrogation(input.gameNo, input.npc_name, input.weapon)

    return {"message": "New interrogation started"}


@router.post("/conversation", 
            )
async def new_interrogation(request: Request, input: ConversationRequest):
    game_service: GameService = request.app.state.game_service
    response = game_service.generation_interrogation_response(input.gameNo, input.npc_name, input.content)
    return response