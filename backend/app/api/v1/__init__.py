from fastapi import APIRouter
from app.api.v1 import auth, experiences

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"]) 