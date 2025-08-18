from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domains.hotels.repository import HotelRepository
from app.domains.hotels.domain import Hotel
from app.infrastructure.database.models import HotelModel

class SQLAlchemyHotelRepository(HotelRepository):
    """SQLAlchemy implementation of HotelRepository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, hotel: Hotel) -> Hotel:
        """Create a new hotel"""
        hotel_model = HotelModel(
            name=hotel.name,
            city=hotel.city
        )
        
        self.session.add(hotel_model)
        self.session.commit()
        self.session.refresh(hotel_model)
        
        return self._to_domain(hotel_model)
    
    async def get_by_id(self, hotel_id: int) -> Optional[Hotel]:
        """Get hotel by ID"""
        hotel_model = self.session.query(HotelModel).filter(HotelModel.id == hotel_id).first()
        
        return self._to_domain(hotel_model) if hotel_model else None
    
    async def get_by_name(self, name: str) -> Optional[Hotel]:
        """Get hotel by name"""
        hotel_model = self.session.query(HotelModel).filter(HotelModel.name == name).first()
        
        return self._to_domain(hotel_model) if hotel_model else None
    
    async def get_all(self) -> List[Hotel]:
        """Get all hotels"""
        hotel_models = self.session.query(HotelModel).all()
        
        return [self._to_domain(hotel_model) for hotel_model in hotel_models]
    
    async def get_by_city(self, city: str) -> List[Hotel]:
        """Get hotels by city"""
        hotel_models = self.session.query(HotelModel).filter(HotelModel.city == city).all()
        
        return [self._to_domain(hotel_model) for hotel_model in hotel_models]
    
    async def update(self, hotel: Hotel) -> Hotel:
        """Update hotel"""
        hotel_model = self.session.query(HotelModel).filter(HotelModel.id == hotel.id).first()
        
        if not hotel_model:
            raise ValueError(f"Hotel with ID {hotel.id} not found")
        
        hotel_model.name = hotel.name
        hotel_model.city = hotel.city
        
        self.session.commit()
        self.session.refresh(hotel_model)
        
        return self._to_domain(hotel_model)
    
    async def delete(self, hotel_id: int) -> bool:
        """Delete hotel by ID"""
        hotel_model = self.session.query(HotelModel).filter(HotelModel.id == hotel_id).first()
        
        if not hotel_model:
            return False
        
        self.session.delete(hotel_model)
        self.session.commit()
        
        return True
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if hotel exists by name"""
        hotel_model = self.session.query(HotelModel).filter(HotelModel.name == name).first()
        return hotel_model is not None
    
    def _to_domain(self, hotel_model: HotelModel) -> Hotel:
        """Convert infrastructure model to domain entity"""
        return Hotel(
            id=hotel_model.id,
            name=hotel_model.name,
            city=hotel_model.city,
            created_at=hotel_model.created_at,
            updated_at=hotel_model.updated_at
        ) 