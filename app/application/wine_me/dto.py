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
    latest_notes: Optional[str] = None
