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