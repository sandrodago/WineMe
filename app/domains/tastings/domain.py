from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..wines.domain import Wine


@dataclass
class Tasting:
    user_id: int
    wine_id: int
    rating: int
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    wine: Optional["Wine"] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def update(self, rating: Optional[int] = None, notes: Optional[str] = None) -> None:
        if rating is not None:
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            self.rating = rating
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.utcnow()


class TastingNotFoundException(Exception):
    pass

