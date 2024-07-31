from fastapi import APIRouter, HTTPException, Request

from app.schemas import game_schema 
from app.services.game_service import GameService


router = APIRouter(
    prefix="/api/v2/in-game",
    tags=["IN_GAME"]
)

# NPC에게 할 질문을 생성하는 라우터
@router.post("/generate-questions", 
            description="NPC에게 할 질문을 생성하는 API 입니다.")
async def generate_questions(request: Request, question_data: game_schema.QuestionRequest):
    game_service: GameService = request.app.state.game_service
    try:
        questions = game_service.generate_npc_questions(
            question_data.gameNo, 
            question_data.npc_name, 
            question_data.keyword, 
            question_data.keyword_type
        )
        return {"questions": questions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# NPC에게 한 질문에 대한 답을 생성하는 라우터
@router.post("/generate-answer", 
            description="NPC에게 한 질문에 대한 답을 생성하는 API 입니다.")
async def talk_to_npc(request: Request, answer_data: game_schema.AnswerRequest):
    game_service: GameService = request.app.state.game_service
    try:
        response = game_service.talk_to_npc(
            answer_data.gameNo, 
            answer_data.npc_name, 
            answer_data.question_index, 
            answer_data.keyword, 
            answer_data.keyword_type
        )
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))