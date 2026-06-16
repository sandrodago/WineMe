from abc import ABC, abstractmethod
from typing import List, Optional

from .domain import Tasting


class TastingRepository(ABC):
    @abstractmethod
    def create(self, tasting: Tasting) -> Tasting:
        pass

    @abstractmethod
    def get_by_id(self, tasting_id: int) -> Optional[Tasting]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Tasting]:
        pass

    @abstractmethod
    def update(self, tasting: Tasting) -> Tasting:
        pass

    @abstractmethod
    def delete(self, tasting_id: int) -> bool:
        pass

