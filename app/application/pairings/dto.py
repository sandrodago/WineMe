from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..wines.dto import WineResponse


@dataclass
class AddPairingRequest:
    wine_id: int
    food: str
    effectiveness: int = 3
    notes: Optional[str] = None


@dataclass
class UpdatePairingRequest:
    food: Optional[str] = None
    effectiveness: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class PairingResponse:
    id: int
    user_id: int
    wine_id: int
    food: str
    effectiveness: int
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    wine: Optional[WineResponse] = None
