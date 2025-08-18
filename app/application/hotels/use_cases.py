from typing import List, Optional
from app.domains.hotels.services import HotelDomainService
from app.domains.hotels.domain import HotelNotFoundException, HotelAlreadyExistsException
from .dto import HotelCreateDTO, HotelUpdateDTO, HotelResponseDTO

class CreateHotelUseCase:
    """Use case for creating a hotel"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, dto: HotelCreateDTO) -> HotelResponseDTO:
        """Execute the create hotel use case"""
        try:
            hotel = await self.hotel_domain_service.create_hotel(
                name=dto.name,
                city=dto.city
            )
            return HotelResponseDTO.from_domain(hotel)
        except HotelAlreadyExistsException as e:
            raise e
        except ValueError as e:
            raise e

class GetHotelUseCase:
    """Use case for getting a hotel by ID"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, hotel_id: int) -> HotelResponseDTO:
        """Execute the get hotel use case"""
        try:
            hotel = await self.hotel_domain_service.get_hotel_by_id(hotel_id)
            return HotelResponseDTO.from_domain(hotel)
        except HotelNotFoundException as e:
            raise e

class UpdateHotelUseCase:
    """Use case for updating a hotel"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, hotel_id: int, dto: HotelUpdateDTO) -> HotelResponseDTO:
        """Execute the update hotel use case"""
        try:
            hotel = await self.hotel_domain_service.update_hotel(
                hotel_id=hotel_id,
                name=dto.name,
                city=dto.city
            )
            return HotelResponseDTO.from_domain(hotel)
        except HotelNotFoundException as e:
            raise e
        except HotelAlreadyExistsException as e:
            raise e
        except ValueError as e:
            raise e

class DeleteHotelUseCase:
    """Use case for deleting a hotel"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, hotel_id: int) -> bool:
        """Execute the delete hotel use case"""
        try:
            return await self.hotel_domain_service.delete_hotel(hotel_id)
        except HotelNotFoundException as e:
            raise e

class ListHotelsUseCase:
    """Use case for listing hotels"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, city_filter: Optional[str] = None) -> List[HotelResponseDTO]:
        """Execute the list hotels use case"""
        try:
            if city_filter:
                hotels = await self.hotel_domain_service.get_hotels_by_city(city_filter)
            else:
                hotels = await self.hotel_domain_service.get_all_hotels()
            
            return [HotelResponseDTO.from_domain(hotel) for hotel in hotels]
        except Exception as e:
            raise e

class SearchHotelsUseCase:
    """Use case for searching hotels"""
    
    def __init__(self, hotel_domain_service: HotelDomainService):
        self.hotel_domain_service = hotel_domain_service
    
    async def execute(self, name_filter: Optional[str] = None, city_filter: Optional[str] = None) -> dict[str, List[HotelResponseDTO]]:
        """Execute the search hotels use case"""
        try:
            hotels = await self.hotel_domain_service.search_hotels(
                name_filter=name_filter,
                city_filter=city_filter
            )
            hotel_by_city = {}
            for hotel in hotels:
                if hotel.city not in hotel_by_city:
                    hotel_by_city[hotel.city] = []
                hotel_by_city[hotel.city].append(hotel)
            return hotel_by_city
        except Exception as e:
            raise e 