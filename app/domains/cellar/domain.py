from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..wines.domain import Wine


@dataclass
class CellarEntry:
    user_id: int
    wine_id: int
    quantity: int = 1
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    wine: Optional["Wine"] = field(default=None, repr=False)

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1")
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def update(self, quantity: Optional[int] = None, notes: Optional[str] = None) -> None:
        if quantity is not None:
            if quantity < 1:
                raise ValueError("Quantity must be at least 1")
            self.quantity = quantity
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.utcnow()


class CellarEntryNotFoundException(Exception):
    pass


class CellarEntryAlreadyExistsException(Exception):
    pass
