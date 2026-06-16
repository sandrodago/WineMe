from pydantic import BaseModel, EmailStr, Field
from typing import Optional
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


# Auth API Schemas
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Cellar API Schemas
class CellarEntryCreateRequest(BaseModel):
    wine_id: int
    quantity: int = Field(default=1, ge=1)
    notes: Optional[str] = None


class CellarEntryUpdateRequest(BaseModel):
    quantity: Optional[int] = Field(default=None, ge=1)
    notes: Optional[str] = None


class CellarEntryResponse(BaseModel):
    id: int
    user_id: int
    wine_id: int
    quantity: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None

    class Config:
        from_attributes = True


# Tasting API Schemas
class TastingCreateRequest(BaseModel):
    wine_id: int
    rating: int = Field(ge=1, le=5)
    notes: Optional[str] = None


class TastingUpdateRequest(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class TastingResponse(BaseModel):
    id: int
    user_id: int
    wine_id: int
    rating: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None

    class Config:
        from_attributes = True


# Pairing API Schemas
class PairingCreateRequest(BaseModel):
    wine_id: int
    food: str
    effectiveness: int = Field(default=3, ge=1, le=5)
    notes: Optional[str] = None


class PairingUpdateRequest(BaseModel):
    food: Optional[str] = None
    effectiveness: Optional[int] = Field(default=None, ge=1, le=5)
    notes: Optional[str] = None


class PairingResponse(BaseModel):
    id: int
    user_id: int
    wine_id: int
    food: str
    effectiveness: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None

    class Config:
        from_attributes = True


class WineMeMatchResponse(BaseModel):
    wine: WineResponse
    match_count: int
    average_effectiveness: float
    latest_pairing_at: datetime
    latest_food: str
    latest_effectiveness: int
    latest_notes: Optional[str] = None

    class Config:
        from_attributes = True
