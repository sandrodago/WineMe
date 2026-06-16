from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..wines.domain import Wine


@dataclass
class Pairing:
    user_id: int
    wine_id: int
    food: str
    effectiveness: int = 3
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    wine: Optional["Wine"] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.food = self.food.strip()
        if not self.food:
            raise ValueError("Food must not be empty")
        if self.effectiveness < 1 or self.effectiveness > 5:
            raise ValueError("Effectiveness must be between 1 and 5")
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def update(
        self,
        food: Optional[str] = None,
        effectiveness: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> None:
        if food is not None:
            food = food.strip()
            if not food:
                raise ValueError("Food must not be empty")
            self.food = food
        if effectiveness is not None:
            if effectiveness < 1 or effectiveness > 5:
                raise ValueError("Effectiveness must be between 1 and 5")
            self.effectiveness = effectiveness
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.utcnow()


class PairingNotFoundException(Exception):
    pass
