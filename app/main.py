from fastapi import FastAPI

from app.api.v1 import user_router, scenario_router, etc_router
from app.api.v2 import in_game_router, new_game_router
from app.core.swagger_config import SwaggerConfig
from app.services.game_service import GameService

swagger_config = SwaggerConfig()
config = swagger_config.get_config()

app = FastAPI(
    title=config["title"],
    description=config["description"],
    version=config["version"],
    license_info=config["license_info"],
    openapi_tags=config["tags_metadata"]
)

# Including API routers
app.include_router(user_router.router)
app.include_router(scenario_router.router)
app.include_router(etc_router.router)
app.include_router(in_game_router.router)
app.include_router(new_game_router.router)

# 전역 GameService 인스턴스 생성
game_service = GameService()

# 모든 라우터에서 game_service에 접근할 수 있도록 설정
app.state.game_service = game_service

@app.on_event("startup")
async def startup_event():
    app.state.game_service = game_service

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)
