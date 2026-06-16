from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..wines.dto import WineResponse


@dataclass
class AddTastingRequest:
    wine_id: int
    rating: int
    notes: Optional[str] = None


@dataclass
class UpdateTastingRequest:
    rating: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class TastingResponse:
    id: int
    user_id: int
    wine_id: int
    rating: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None

