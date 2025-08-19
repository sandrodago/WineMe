from abc import ABC, abstractmethod
from typing import List, Optional
from .domain import Wine

class WinesRepository(ABC):
    """Wine repository interface"""
    
    @abstractmethod
    def create(self, wine: Wine) -> Wine:
        pass
    
    @abstractmethod
    def get_by_id(self, wine_id: int) -> Optional[Wine]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Wine]:
        pass
    
    @abstractmethod
    def update(self, wine: Wine) -> Wine:
        pass
    
    @abstractmethod
    def delete(self, wine_id: int) -> bool:
        pass
