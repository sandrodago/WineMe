from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User API Schemas
class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    password: str

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
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

# Wine API Schemas
class WineCreateRequest(BaseModel):
    name: str
    year: int
    grape: str
    country: str
    region: str
    color: str
    description: Optional[str] = None

class WineUpdateRequest(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

class WineResponse(BaseModel):
    id: int
    name: str
    year: int
    grape: str
    country: str
    region: str
    color: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True 