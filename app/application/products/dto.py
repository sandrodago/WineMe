from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CreateProductRequest:
    """DTO for creating a product"""
    name: str
    category: str
    price: float
    description: Optional[str] = None
    stock_quantity: int = 0

@dataclass
class UpdateProductRequest:
    """DTO for updating a product"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

@dataclass
class ProductResponse:
    """DTO for product response"""
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] 