from sqlalchemy.orm import Session
from ..infrastructure.database.connection import get_db
from ..infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from ..infrastructure.repositories.product_repository import SQLAlchemyProductRepository
from ..infrastructure.repositories.hotel_repository import SQLAlchemyHotelRepository
from ..domains.users.services import UserService
from ..domains.products.services import ProductService
from ..domains.hotels.services import HotelDomainService

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
    
    def get_product_service(self, db: Session) -> ProductService:
        """Get product service with repository"""
        if 'product_service' not in self._services:
            product_repository = SQLAlchemyProductRepository(db)
            self._services['product_service'] = ProductService(product_repository)
        return self._services['product_service']
    
    def get_hotel_domain_service(self, session: Session) -> HotelDomainService:
        """Get hotel domain service with repository"""
        if 'hotel_domain_service' not in self._services:
            hotel_repository = SQLAlchemyHotelRepository(session)
            self._services['hotel_domain_service'] = HotelDomainService(hotel_repository)
        return self._services['hotel_domain_service']

# Global container instance
container = Container()

# Dependency injection functions
def get_session() -> Session:
    """Get database session"""
    return next(get_db())

def get_hotel_domain_service(session: Session) -> HotelDomainService:
    """Get hotel domain service"""
    return container.get_hotel_domain_service(session) 