from typing import List, Optional
from .domain import Hotel, HotelNotFoundException, HotelAlreadyExistsException
from .repository import HotelRepository

class HotelDomainService:
    """Domain service for Hotel business logic"""
    
    def __init__(self, hotel_repository: HotelRepository):
        self.hotel_repository = hotel_repository
    
    async def create_hotel(self, name: str, city: str) -> Hotel:
        """Create a new hotel with validation"""
        # Check if hotel with same name already exists
        if await self.hotel_repository.exists_by_name(name):
            raise HotelAlreadyExistsException(f"Hotel with name '{name}' already exists")
        
        hotel = Hotel(name=name, city=city)
        return await self.hotel_repository.create(hotel)
    
    async def get_hotel_by_id(self, hotel_id: int) -> Hotel:
        """Get hotel by ID with validation"""
        hotel = await self.hotel_repository.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundException(f"Hotel with ID {hotel_id} not found")
        return hotel
    
    async def get_hotel_by_name(self, name: str) -> Hotel:
        """Get hotel by name with validation"""
        hotel = await self.hotel_repository.get_by_name(name)
        if not hotel:
            raise HotelNotFoundException(f"Hotel with name '{name}' not found")
        return hotel
    
    async def get_all_hotels(self) -> List[Hotel]:
        """Get all hotels"""
        return await self.hotel_repository.get_all()
    
    async def get_hotels_by_city(self, city: str) -> List[Hotel]:
        """Get hotels by city"""
        return await self.hotel_repository.get_by_city(city)
    
    async def update_hotel(self, hotel_id: int, name: Optional[str] = None, city: Optional[str] = None) -> Hotel:
        """Update hotel with validation"""
        hotel = await self.get_hotel_by_id(hotel_id)
        
        # Check if new name conflicts with existing hotel (excluding current hotel)
        if name is not None:
            existing_hotel = await self.hotel_repository.get_by_name(name)
            if existing_hotel and existing_hotel.id != hotel_id:
                raise HotelAlreadyExistsException(f"Hotel with name '{name}' already exists")
        
        hotel.update_details(name=name, city=city)
        return await self.hotel_repository.update(hotel)
    
    async def delete_hotel(self, hotel_id: int) -> bool:
        """Delete hotel with validation"""
        hotel = await self.get_hotel_by_id(hotel_id)
        return await self.hotel_repository.delete(hotel_id)
    
    async def search_hotels(self, name_filter: Optional[str] = None, city_filter: Optional[str] = None) -> List[Hotel]:
        """Search hotels by name and/or city filters"""
        if city_filter:
            hotels = await self.hotel_repository.get_by_city(city_filter)
        else:
            hotels = await self.hotel_repository.get_all()
        
        if name_filter:
            hotels = [hotel for hotel in hotels if name_filter.lower() in hotel.name.lower()]
        
        return hotels[:5]