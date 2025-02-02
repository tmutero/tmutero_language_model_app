from fastapi import APIRouter

from app.routers import user
from app.routers import language_model
from app.routers import threat_modelling_ai


from app.settings import settings


api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(user.router)
api_router.include_router(language_model.router)
api_router.include_router(threat_modelling_ai.router)

