from fastapi import FastAPI

from app.api import user_router
from app.api import scenario_router
from app.api import etc_router
from app.core.swagger_config import SwaggerConfig


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)
