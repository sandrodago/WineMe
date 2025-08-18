from abc import ABC, abstractmethod
from typing import List, Optional
from .domain import Product, ProductCategory

class ProductRepository(ABC):
    """Product repository interface - defines contract for product data access"""
    
    @abstractmethod
    def create(self, product: Product) -> Product:
        """Create a new product"""
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        pass
    
    @abstractmethod
    def get_by_category(self, category: ProductCategory, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products by category"""
        pass
    
    @abstractmethod
    def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get only active products"""
        pass
    
    @abstractmethod
    def update(self, product: Product) -> Product:
        """Update product"""
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete product"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if product exists by name"""
        pass 