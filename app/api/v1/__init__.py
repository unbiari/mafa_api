from fastapi import APIRouter

from .controller import router as controller_router

api_v1_router = APIRouter()

api_v1_router.include_router(controller_router)
