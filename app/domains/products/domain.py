from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

# Value Objects
@dataclass(frozen=True)
class ProductName:
    """Product name value object with validation"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid_name(self.value):
            raise ValueError(f"Invalid product name: {self.value}")
    
    @staticmethod
    def _is_valid_name(name: str) -> bool:
        return len(name.strip()) >= 1 and len(name) <= 100
    
    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class ProductCategory:
    """Product category value object"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid_category(self.value):
            raise ValueError(f"Invalid product category: {self.value}")
    
    @staticmethod
    def _is_valid_category(category: str) -> bool:
        return len(category.strip()) >= 1 and len(category) <= 50
    
    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class Price:
    """Price value object with validation"""
    value: float
    
    def __post_init__(self):
        if not self._is_valid_price(self.value):
            raise ValueError(f"Invalid price: {self.value}")
    
    @staticmethod
    def _is_valid_price(price: float) -> bool:
        return price >= 0.0
    
    def __str__(self) -> str:
        return f"${self.value:.2f}"

# Domain Entity
@dataclass
class Product:
    """Product domain entity with business logic"""
    
    name: ProductName
    category: ProductCategory
    price: Price
    description: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the product"""
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the product"""
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.utcnow()
    
    def update_stock(self, quantity: int) -> None:
        """Update stock quantity"""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self.stock_quantity = quantity
        self.updated_at = datetime.utcnow()
    
    def add_stock(self, quantity: int) -> None:
        """Add stock to existing quantity"""
        if quantity < 0:
            raise ValueError("Cannot add negative stock")
        self.stock_quantity += quantity
        self.updated_at = datetime.utcnow()
    
    def remove_stock(self, quantity: int) -> None:
        """Remove stock from existing quantity"""
        if quantity < 0:
            raise ValueError("Cannot remove negative stock")
        if self.stock_quantity < quantity:
            raise ValueError("Insufficient stock")
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()
    
    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        return self.stock_quantity > 0 and self.is_active
    
    def update_price(self, new_price: float) -> None:
        """Update product price"""
        self.price = Price(new_price)
        self.updated_at = datetime.utcnow()
    
    def update_details(self, name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None) -> None:
        """Update product details"""
        if name is not None:
            self.name = ProductName(name)
        if description is not None:
            self.description = description
        if category is not None:
            self.category = ProductCategory(category)
        self.updated_at = datetime.utcnow()

# Domain Exceptions
class ProductNotFoundException(Exception):
    """Raised when a product is not found"""
    pass

class ProductAlreadyExistsException(Exception):
    """Raised when trying to create a product that already exists"""
    pass

class InsufficientStockException(Exception):
    """Raised when trying to remove more stock than available"""
    pass 