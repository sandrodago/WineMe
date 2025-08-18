from sqlalchemy.orm import Session
from ..infrastructure.database.connection import get_db
from ..infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from ..domains.users.services import UserService

class Container:
    """Simple dependency injection container"""
    
    def __init__(self):
        self._services = {}
    
    def get_user_service(self, db: Session) -> UserService:
        """Get user service with repository"""
        if 'user_service' not in self._services:
            user_repository = SQLAlchemyUserRepository(db)
            self._services['user_service'] = UserService(user_repository)
        return self._services['user_service']

# Global container instance
container = Container()

# Dependency injection functions
def get_session() -> Session:
    """Get database session"""
    return next(get_db()) 