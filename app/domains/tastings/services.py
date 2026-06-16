from typing import List, Optional

from ..wines.services import WineService
from .domain import Tasting, TastingNotFoundException
from .repository import TastingRepository


class TastingService:
    def __init__(self, tasting_repository: TastingRepository, wine_service: WineService):
        self.tasting_repository = tasting_repository
        self.wine_service = wine_service

    def add_tasting(
        self,
        user_id: int,
        wine_id: int,
        rating: int,
        notes: Optional[str] = None,
    ) -> Tasting:
        self.wine_service.get_wine_by_id(wine_id)
        tasting = Tasting(user_id=user_id, wine_id=wine_id, rating=rating, notes=notes)
        return self.tasting_repository.create(tasting)

    def get_tasting(self, user_id: int, tasting_id: int) -> Tasting:
        tasting = self.tasting_repository.get_by_id(tasting_id)
        if not tasting or tasting.user_id != user_id:
            raise TastingNotFoundException(f"Tasting {tasting_id} not found")
        return tasting

    def get_tastings(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Tasting]:
        return self.tasting_repository.get_by_user(user_id, skip=skip, limit=limit)

    def get_tastings_for_wines(self, user_id: int, wine_ids: List[int]) -> List[Tasting]:
        return self.tasting_repository.get_by_user_and_wines(user_id, wine_ids)

    def update_tasting(
        self,
        user_id: int,
        tasting_id: int,
        rating: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> Tasting:
        tasting = self.get_tasting(user_id, tasting_id)
        tasting.update(rating=rating, notes=notes)
        return self.tasting_repository.update(tasting)

    def remove_tasting(self, user_id: int, tasting_id: int) -> bool:
        self.get_tasting(user_id, tasting_id)
        return self.tasting_repository.delete(tasting_id)
