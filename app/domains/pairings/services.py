from typing import List, Optional

from ..wines.services import WineService
from .domain import Pairing, PairingNotFoundException
from .repository import PairingRepository


class PairingService:
    def __init__(self, pairing_repository: PairingRepository, wine_service: WineService):
        self.pairing_repository = pairing_repository
        self.wine_service = wine_service

    def add_pairing(
        self,
        user_id: int,
        wine_id: int,
        food: str,
        effectiveness: int = 3,
        notes: Optional[str] = None,
    ) -> Pairing:
        self.wine_service.get_wine_by_id(wine_id)
        pairing = Pairing(
            user_id=user_id,
            wine_id=wine_id,
            food=food,
            effectiveness=effectiveness,
            notes=notes,
        )
        return self.pairing_repository.create(pairing)

    def get_pairing(self, user_id: int, pairing_id: int) -> Pairing:
        pairing = self.pairing_repository.get_by_id(pairing_id)
        if not pairing or pairing.user_id != user_id:
            raise PairingNotFoundException(f"Pairing {pairing_id} not found")
        return pairing

    def get_pairings(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Pairing]:
        return self.pairing_repository.get_by_user(user_id, skip=skip, limit=limit)

    def search_pairings_by_food(
        self, user_id: int, food: str, skip: int = 0, limit: int = 100
    ) -> List[Pairing]:
        return self.pairing_repository.search_by_food(user_id, food, skip=skip, limit=limit)

    def update_pairing(
        self,
        user_id: int,
        pairing_id: int,
        food: Optional[str] = None,
        effectiveness: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> Pairing:
        pairing = self.get_pairing(user_id, pairing_id)
        pairing.update(food=food, effectiveness=effectiveness, notes=notes)
        return self.pairing_repository.update(pairing)

    def remove_pairing(self, user_id: int, pairing_id: int) -> bool:
        self.get_pairing(user_id, pairing_id)
        return self.pairing_repository.delete(pairing_id)
