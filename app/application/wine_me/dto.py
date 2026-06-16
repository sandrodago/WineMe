from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..wines.dto import WineResponse


@dataclass
class WineMeMatchResponse:
    wine: WineResponse
    match_count: int
    average_effectiveness: float
    latest_pairing_at: datetime
    latest_food: str
    latest_effectiveness: int
    average_tasting_rating: Optional[float] = None
    latest_tasting_at: Optional[datetime] = None
    latest_tasting_rating: Optional[int] = None
    latest_notes: Optional[str] = None
    score: Optional[float] = None
