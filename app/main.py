from fastapi import FastAPI
import uvicorn
import asyncio

from app.middleware import CustomMiddleware
from domain.user import user_router
from domain.scenario import scenario_router
from domain.etc import etc_router

from discord_bot.discord_bot import run
from lib.logging_config import configure_logging


description = """
#### 두근두근 놀러와요 마피아의 숲! 베어머더러! 지금 플레이하세요(찡긋)

기능 목록:

* **Say Hello** (_completely implemented_).
* **scenario** (_not implemented_).
* **user** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "scenario",
        "description": "게임 진행을 위한 시나리오 등을 생성합니다."
    },
    {
        "name": "user",
        "description": "사용자와 상호작용 할 수 있도록 답변을 생성합니다."
    },
]

app = FastAPI(
    title="AI Mafia",
    description=description,
    version="0.1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)


@app.on_event("startup")
async def startup_event():
    # Configure logging on startup
    configure_logging()


# Adding middleware for additional request/response processing
# app.add_middleware(CustomMiddleware)

# Starting Discord bot asynchronously
# asyncio.create_task(run())

# Including API routers
app.include_router(user_router.router)
app.include_router(scenario_router.router)
app.include_router(etc_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)