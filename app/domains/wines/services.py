from typing import List, Optional
from .domain import Wine
from .repository import WinesRepository
from datetime import datetime

class WineService:
    """Wine domain service - contains business logic for wine operations"""
    
    def __init__(self, wine_repository: WinesRepository):
        self.wine_repository = wine_repository
    
    def create_wine(self, name: str, year: int, grape: str, country: str, region: str, color: str, description: Optional[str] = None) -> Wine:
        """Create a new wine with business rules"""
        # Check business rules
        if self.wine_repository.exists_by_name(name):
            raise ValueError(f"Wine with name {name} already exists")
        
        # Create domain entity
        wine = Wine(
            name=name,
            year=year,
            grape=grape,
            country=country,
            region=region,
            color=color,
            description=description
        )
        
        # Save to repository
        return self.wine_repository.create(wine)
    
    def get_wine_by_id(self, wine_id: int) -> Wine:
        """Get wine by ID"""
        wine = self.wine_repository.get_by_id(wine_id)
        if not wine:
            raise ValueError(f"Wine with ID {wine_id} not found")
        return wine
    
    def get_all_wines(self, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get all wines with pagination"""
        return self.wine_repository.get_all(skip=skip, limit=limit)
    
    def get_wines_by_country(self, country: str, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get wines by country"""
        return self.wine_repository.get_by_country(country, skip=skip, limit=limit)
    
    def get_wines_by_grape(self, grape: str, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get wines by grape variety"""
        return self.wine_repository.get_by_grape(grape, skip=skip, limit=limit)
    
    def update_wine(self, wine_id: int, name: Optional[str] = None, year: Optional[int] = None, 
                   grape: Optional[str] = None, country: Optional[str] = None, 
                   region: Optional[str] = None, color: Optional[str] = None, 
                   description: Optional[str] = None) -> Wine:
        """Update wine with business logic"""
        wine = self.get_wine_by_id(wine_id)
        
        # Update fields if provided
        if name is not None:
            wine.name = name
        if year is not None:
            wine.year = year
        if grape is not None:
            wine.grape = grape
        if country is not None:
            wine.country = country
        if region is not None:
            wine.region = region
        if color is not None:
            wine.color = color
        if description is not None:
            wine.description = description
        
        wine.updated_at = datetime.utcnow()
        
        return self.wine_repository.update(wine)
    
    def delete_wine(self, wine_id: int) -> bool:
        """Delete wine"""
        wine = self.get_wine_by_id(wine_id)
        return self.wine_repository.delete(wine_id)
