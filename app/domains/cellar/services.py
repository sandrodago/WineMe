from typing import List, Optional

from ..wines.services import WineService
from .domain import (
    CellarEntry,
    CellarEntryAlreadyExistsException,
    CellarEntryNotFoundException,
)
from .repository import CellarRepository


class CellarService:
    def __init__(self, cellar_repository: CellarRepository, wine_service: WineService):
        self.cellar_repository = cellar_repository
        self.wine_service = wine_service

    def add_to_cellar(
        self,
        user_id: int,
        wine_id: int,
        quantity: int = 1,
        notes: Optional[str] = None,
    ) -> CellarEntry:
        self.wine_service.get_wine_by_id(wine_id)

        existing = self.cellar_repository.get_by_user_and_wine(user_id, wine_id)
        if existing:
            raise CellarEntryAlreadyExistsException(
                f"Wine {wine_id} is already in your cellar"
            )

        entry = CellarEntry(
            user_id=user_id,
            wine_id=wine_id,
            quantity=quantity,
            notes=notes,
        )
        return self.cellar_repository.create(entry)

    def get_entry(self, user_id: int, entry_id: int) -> CellarEntry:
        entry = self.cellar_repository.get_by_id(entry_id)
        if not entry or entry.user_id != user_id:
            raise CellarEntryNotFoundException(f"Cellar entry {entry_id} not found")
        return entry

    def get_cellar(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CellarEntry]:
        return self.cellar_repository.get_by_user(user_id, skip=skip, limit=limit)

    def update_entry(
        self,
        user_id: int,
        entry_id: int,
        quantity: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> CellarEntry:
        entry = self.get_entry(user_id, entry_id)
        entry.update(quantity=quantity, notes=notes)
        return self.cellar_repository.update(entry)

    def remove_from_cellar(self, user_id: int, entry_id: int) -> bool:
        self.get_entry(user_id, entry_id)
        return self.cellar_repository.delete(entry_id)
