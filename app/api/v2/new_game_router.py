from fastapi import APIRouter, HTTPException, Request

from app.schemas import game_schema 
from app.services.game_service import GameService


router = APIRouter(
    prefix="/api/v2/new-game",
    tags=["NEW_GAME"]
)

# 새로운 게임을 시작하는 라우터
@router.post("/start", 
            description="새로운 게임을 시작하며 게임을 생성하는 API 입니다.")
async def start_game(request: Request, game_data: game_schema.GameStartRequest):
    game_service: GameService = request.app.state.game_service
    if game_data.language not in ["en", "ko"]:
        raise HTTPException(status_code=400, detail="Invalid language. Choose 'en' or 'ko'.")
    try:
        game_state = game_service.initialize_new_game(game_data)
        return {"answer": game_state['first_blood']}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 시나리오를 생성하는 라우터
@router.post("/generate-scenario", 
            description="해당 게임의 상태에 따라 시나리오를 생성하는 API 입니다.")
def generate_scenario(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        scenario = game_service.generate_game_scenario(game_data.gameNo)
        return {"scenario": scenario}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 촌장의 편지를 생성하는 라우터
@router.post("/generate-chief-letter", 
            description="해당 게임의 상태에 따라 촌장의 편지를 생성하는 API 입니다.")
def generate_chief_letter(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        chief_letter = game_service.generate_chief_letter(game_data.gameNo)
        return {"answer": chief_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 게임 상태를 확인하는 라우터
@router.post("/status", 
            description="해당 게임의 상태를 확인하는 API 입니다.")
def get_game_status(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        status = game_service.get_game_status(game_data.gameNo)
        return status
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 게임 진행을 다음 날로 넘기는 라우터
@router.post("/next_day", 
            description="해당 게임의 상태를 다음 날로 넘기는 API 입니다.")
def next_day(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        result = game_service.proceed_to_next_day(game_data.gameNo)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 게임 진행 상황을 저장하는 라우터
# @router.post("/save-progress", 
#             description="해당 게임의 상태를 저장하는 API 입니다.")
def save_progress(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        game_state = game_service.get_game_status(game_data.gameNo)
        result = game_service.save_game_progress(game_data.gameNo, game_state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 알리바이와 목격자 정보를 생성하는 라우터
@router.post("/generate-alibis-and-witness", 
            description="해당 게임의 알리바이와 목격자 정보를 생성하는 API입니다.")
async def generate_alibis_and_witness(request: Request, game_data: game_schema.GameRequest):
    game_service: GameService = request.app.state.game_service
    try:
        alibis_and_witness = game_service.generate_alibis_and_witness(game_data.gameNo)
        return alibis_and_witness
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))