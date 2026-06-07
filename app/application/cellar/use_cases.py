from typing import List

from ...domains.cellar.domain import (
    CellarEntryAlreadyExistsException,
    CellarEntryNotFoundException,
)
from ...domains.cellar.services import CellarService
from ..wines.dto import WineResponse
from .dto import AddToCellarRequest, CellarEntryResponse, UpdateCellarEntryRequest


class AddToCellarUseCase:
    def __init__(self, cellar_service: CellarService):
        self.cellar_service = cellar_service

    def execute(self, user_id: int, request: AddToCellarRequest) -> CellarEntryResponse:
        entry = self.cellar_service.add_to_cellar(
            user_id=user_id,
            wine_id=request.wine_id,
            quantity=request.quantity,
            notes=request.notes,
        )
        return _to_response(entry, include_wine=True)


class GetCellarUseCase:
    def __init__(self, cellar_service: CellarService):
        self.cellar_service = cellar_service

    def execute(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CellarEntryResponse]:
        entries = self.cellar_service.get_cellar(user_id, skip=skip, limit=limit)
        return [_to_response(entry, include_wine=True) for entry in entries]


class GetCellarEntryUseCase:
    def __init__(self, cellar_service: CellarService):
        self.cellar_service = cellar_service

    def execute(self, user_id: int, entry_id: int) -> CellarEntryResponse:
        entry = self.cellar_service.get_entry(user_id, entry_id)
        return _to_response(entry, include_wine=True)


class UpdateCellarEntryUseCase:
    def __init__(self, cellar_service: CellarService):
        self.cellar_service = cellar_service

    def execute(
        self, user_id: int, entry_id: int, request: UpdateCellarEntryRequest
    ) -> CellarEntryResponse:
        entry = self.cellar_service.update_entry(
            user_id=user_id,
            entry_id=entry_id,
            quantity=request.quantity,
            notes=request.notes,
        )
        return _to_response(entry, include_wine=True)


class RemoveFromCellarUseCase:
    def __init__(self, cellar_service: CellarService):
        self.cellar_service = cellar_service

    def execute(self, user_id: int, entry_id: int) -> bool:
        return self.cellar_service.remove_from_cellar(user_id, entry_id)


def _to_response(entry, include_wine: bool = False) -> CellarEntryResponse:
    wine = None
    if include_wine and entry.wine:
        wine_data = entry.wine
        if wine_data:
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

    return CellarEntryResponse(
        id=entry.id,
        user_id=entry.user_id,
        wine_id=entry.wine_id,
        quantity=entry.quantity,
        notes=entry.notes,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        wine=wine,
    )
