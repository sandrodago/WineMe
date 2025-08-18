from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User API Schemas
class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    display_name: str
    
    class Config:
        from_attributes = True

# Product API Schemas
class ProductCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock_quantity: int = 0
    is_active: bool = True

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Hotel API Schemas
class HotelCreate(BaseModel):
    name: str
    city: str

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None

class HotelResponse(BaseModel):
    id: int
    name: str
    city: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True 