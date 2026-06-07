from abc import ABC, abstractmethod
from typing import List, Optional

from .domain import CellarEntry


class CellarRepository(ABC):
    @abstractmethod
    def create(self, entry: CellarEntry) -> CellarEntry:
        pass

    @abstractmethod
    def get_by_id(self, entry_id: int) -> Optional[CellarEntry]:
        pass

    @abstractmethod
    def get_by_user_and_wine(self, user_id: int, wine_id: int) -> Optional[CellarEntry]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CellarEntry]:
        pass

    @abstractmethod
    def update(self, entry: CellarEntry) -> CellarEntry:
        pass

    @abstractmethod
    def delete(self, entry_id: int) -> bool:
        pass
