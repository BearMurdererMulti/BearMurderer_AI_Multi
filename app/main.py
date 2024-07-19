from fastapi import FastAPI
import uvicorn

from app.domain.user import user_router
from app.domain.scenario import scenario_router
from app.domain.etc import etc_router


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

# Including API routers
app.include_router(user_router.router)
app.include_router(scenario_router.router)
app.include_router(etc_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)