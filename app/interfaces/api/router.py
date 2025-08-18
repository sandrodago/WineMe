from fastapi import APIRouter
from .controllers import users_controller, products_controller, hotels_controller

api_router = APIRouter()

# Include domain controllers
api_router.include_router(users_controller.router, prefix="/users", tags=["users"])
api_router.include_router(products_controller.router, prefix="/products", tags=["products"])
api_router.include_router(hotels_controller.router, prefix="/hotels", tags=["hotels"])