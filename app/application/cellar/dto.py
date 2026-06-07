from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..wines.dto import WineResponse


@dataclass
class AddToCellarRequest:
    wine_id: int
    quantity: int = 1
    notes: Optional[str] = None


@dataclass
class UpdateCellarEntryRequest:
    quantity: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class CellarEntryResponse:
    id: int
    user_id: int
    wine_id: int
    quantity: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None
