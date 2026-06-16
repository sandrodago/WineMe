from abc import ABC, abstractmethod
from typing import List, Optional

from .domain import Pairing


class PairingRepository(ABC):
    @abstractmethod
    def create(self, pairing: Pairing) -> Pairing:
        pass

    @abstractmethod
    def get_by_id(self, pairing_id: int) -> Optional[Pairing]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Pairing]:
        pass

    @abstractmethod
    def search_by_food(self, user_id: int, food: str, skip: int = 0, limit: Optional[int] = 100) -> List[Pairing]:
        pass

    @abstractmethod
    def update(self, pairing: Pairing) -> Pairing:
        pass

    @abstractmethod
    def delete(self, pairing_id: int) -> bool:
        pass
