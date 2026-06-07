from fastapi import APIRouter
from .controllers import auth_controller, cellar_controller, users_controller, wines_controller

api_router = APIRouter()

api_router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
api_router.include_router(cellar_controller.router, prefix="/cellar", tags=["cellar"])
api_router.include_router(users_controller.router, prefix="/users", tags=["users"])
api_router.include_router(wines_controller.router, prefix="/wines", tags=["wines"])