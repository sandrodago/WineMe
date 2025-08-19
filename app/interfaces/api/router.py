from fastapi import APIRouter
from .controllers import users_controller, wines_controller

api_router = APIRouter()

# Include domain controllers
api_router.include_router(users_controller.router, prefix="/users", tags=["users"])
api_router.include_router(wines_controller.router, prefix="/wines", tags=["wines"])