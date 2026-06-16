from typing import List, Optional

from .domain import Pairing, PairingNotFoundException, WineMeMatch
from ..wines.services import WineService
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

    def search_wine_me(
        self, user_id: int, food: str, skip: int = 0, limit: int = 100
    ) -> List[WineMeMatch]:
        pairings = self.search_pairings_by_food(user_id, food, skip=0, limit=None)
        grouped = {}

        for pairing in pairings:
            bucket = grouped.setdefault(
                pairing.wine_id,
                {
                    "wine": pairing.wine,
                    "count": 0,
                    "effectiveness_sum": 0,
                    "latest_pairing_at": pairing.created_at,
                    "latest_food": pairing.food,
                    "latest_effectiveness": pairing.effectiveness,
                    "latest_notes": pairing.notes,
                },
            )

            bucket["count"] += 1
            bucket["effectiveness_sum"] += pairing.effectiveness

            if pairing.created_at and pairing.created_at > bucket["latest_pairing_at"]:
                bucket["latest_pairing_at"] = pairing.created_at
                bucket["latest_food"] = pairing.food
                bucket["latest_effectiveness"] = pairing.effectiveness
                bucket["latest_notes"] = pairing.notes

        results = [
            WineMeMatch(
                wine=data["wine"],
                match_count=data["count"],
                average_effectiveness=round(data["effectiveness_sum"] / data["count"], 2),
                latest_pairing_at=data["latest_pairing_at"],
                latest_food=data["latest_food"],
                latest_effectiveness=data["latest_effectiveness"],
                latest_notes=data["latest_notes"],
            )
            for data in grouped.values()
            if data["wine"] is not None
        ]

        results.sort(
            key=lambda item: (
                item.average_effectiveness,
                item.latest_pairing_at,
                item.match_count,
            ),
            reverse=True,
        )
        return results[skip: skip + limit]

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
