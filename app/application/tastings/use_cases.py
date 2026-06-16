from typing import List

from ...domains.tastings.domain import TastingNotFoundException
from ...domains.tastings.services import TastingService
from ..wines.dto import WineResponse
from .dto import AddTastingRequest, TastingResponse, UpdateTastingRequest


class AddTastingUseCase:
    def __init__(self, tasting_service: TastingService):
        self.tasting_service = tasting_service

    def execute(self, user_id: int, request: AddTastingRequest) -> TastingResponse:
        tasting = self.tasting_service.add_tasting(
            user_id=user_id,
            wine_id=request.wine_id,
            rating=request.rating,
            notes=request.notes,
        )
        return _to_response(tasting, include_wine=True)


class GetTastingsUseCase:
    def __init__(self, tasting_service: TastingService):
        self.tasting_service = tasting_service

    def execute(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TastingResponse]:
        tastings = self.tasting_service.get_tastings(user_id, skip=skip, limit=limit)
        return [_to_response(tasting, include_wine=True) for tasting in tastings]


class GetTastingUseCase:
    def __init__(self, tasting_service: TastingService):
        self.tasting_service = tasting_service

    def execute(self, user_id: int, tasting_id: int) -> TastingResponse:
        tasting = self.tasting_service.get_tasting(user_id, tasting_id)
        return _to_response(tasting, include_wine=True)


class UpdateTastingUseCase:
    def __init__(self, tasting_service: TastingService):
        self.tasting_service = tasting_service

    def execute(self, user_id: int, tasting_id: int, request: UpdateTastingRequest) -> TastingResponse:
        tasting = self.tasting_service.update_tasting(
            user_id=user_id,
            tasting_id=tasting_id,
            rating=request.rating,
            notes=request.notes,
        )
        return _to_response(tasting, include_wine=True)


class DeleteTastingUseCase:
    def __init__(self, tasting_service: TastingService):
        self.tasting_service = tasting_service

    def execute(self, user_id: int, tasting_id: int) -> bool:
        return self.tasting_service.remove_tasting(user_id, tasting_id)


def _to_response(tasting, include_wine: bool = False) -> TastingResponse:
    wine = None
    if include_wine and tasting.wine:
        wine_data = tasting.wine
        wine = WineResponse(
            id=wine_data.id,
            name=wine_data.name,
            year=wine_data.year,
            grape=wine_data.grape,
            country=wine_data.country,
            region=wine_data.region,
            color=wine_data.color,
            description=wine_data.description,
            created_at=wine_data.created_at,
            updated_at=wine_data.updated_at,
        )

    return TastingResponse(
        id=tasting.id,
        user_id=tasting.user_id,
        wine_id=tasting.wine_id,
        rating=tasting.rating,
        notes=tasting.notes,
        created_at=tasting.created_at,
        updated_at=tasting.updated_at,
        wine=wine,
    )

