from fastapi import FastAPI
from api_service.config.config import settings
from api_service.api.v1.api import api_router as api_router_v1

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router_v1, prefix=settings.API_V1_STR)