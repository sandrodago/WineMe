from typing import List, Optional
from ...domains.wines.services import WineService
from .dto import CreateWineRequest, UpdateWineRequest, WineResponse

class CreateWineUseCase:
    """Use case for creating a wine"""
    
    def __init__(self, wine_service: WineService):
        self.wine_service = wine_service
    
    def execute(self, request: CreateWineRequest) -> WineResponse:
        """Execute the create wine use case"""
        try:
            wine = self.wine_service.create_wine(
                name=request.name,
                year=request.year,
                grape=request.grape,
                country=request.country,
                region=request.region,
                color=request.color,
                description=request.description
            )
            return self._to_response(wine)
        except ValueError as e:
            raise e
    
    def _to_response(self, wine) -> WineResponse:
        return WineResponse(
            id=wine.id,
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description,
            created_at=wine.created_at,
            updated_at=wine.updated_at
        )

class GetWineUseCase:
    """Use case for getting a wine by ID"""
    
    def __init__(self, wine_service: WineService):
        self.wine_service = wine_service
    
    def execute(self, wine_id: int) -> WineResponse:
        """Execute the get wine use case"""
        try:
            wine = self.wine_service.get_wine_by_id(wine_id)
            return self._to_response(wine)
        except ValueError as e:
            raise e
    
    def _to_response(self, wine) -> WineResponse:
        return WineResponse(
            id=wine.id,
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description,
            created_at=wine.created_at,
            updated_at=wine.updated_at
        )

class GetWinesUseCase:
    """Use case for getting all wines"""
    
    def __init__(self, wine_service: WineService):
        self.wine_service = wine_service
    
    def execute(self, skip: int = 0, limit: int = 100) -> List[WineResponse]:
        """Execute the get wines use case"""
        wines = self.wine_service.get_all_wines(skip=skip, limit=limit)
        return [self._to_response(wine) for wine in wines]
    
    def _to_response(self, wine) -> WineResponse:
        return WineResponse(
            id=wine.id,
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description,
            created_at=wine.created_at,
            updated_at=wine.updated_at
        )

class UpdateWineUseCase:
    """Use case for updating a wine"""
    
    def __init__(self, wine_service: WineService):
        self.wine_service = wine_service
    
    def execute(self, wine_id: int, request: UpdateWineRequest) -> WineResponse:
        """Execute the update wine use case"""
        try:
            wine = self.wine_service.update_wine(
                wine_id=wine_id,
                name=request.name,
                year=request.year,
                grape=request.grape,
                country=request.country,
                region=request.region,
                color=request.color,
                description=request.description
            )
            return self._to_response(wine)
        except ValueError as e:
            raise e
    
    def _to_response(self, wine) -> WineResponse:
        return WineResponse(
            id=wine.id,
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description,
            created_at=wine.created_at,
            updated_at=wine.updated_at
        )

class DeleteWineUseCase:
    """Use case for deleting a wine"""
    
    def __init__(self, wine_service: WineService):
        self.wine_service = wine_service
    
    def execute(self, wine_id: int) -> bool:
        """Execute the delete wine use case"""
        try:
            return self.wine_service.delete_wine(wine_id)
        except ValueError as e:
            raise e
