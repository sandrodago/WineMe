from typing import List

from ...domains.pairings.services import PairingService
from .dto import AddPairingRequest, PairingResponse, UpdatePairingRequest
from ..wines.dto import WineResponse


class AddPairingUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, request: AddPairingRequest) -> PairingResponse:
        pairing = self.pairing_service.add_pairing(
            user_id=user_id,
            wine_id=request.wine_id,
            food=request.food,
            effectiveness=request.effectiveness,
            notes=request.notes,
        )
        return _to_response(pairing, include_wine=True)


class GetPairingsUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, skip: int = 0, limit: int = 100) -> List[PairingResponse]:
        pairings = self.pairing_service.get_pairings(user_id, skip=skip, limit=limit)
        return [_to_response(pairing, include_wine=True) for pairing in pairings]


class SearchPairingsUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, food: str, skip: int = 0, limit: int = 100) -> List[PairingResponse]:
        pairings = self.pairing_service.search_pairings_by_food(user_id, food, skip=skip, limit=limit)
        return [_to_response(pairing, include_wine=True) for pairing in pairings]


class GetPairingUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, pairing_id: int) -> PairingResponse:
        pairing = self.pairing_service.get_pairing(user_id, pairing_id)
        return _to_response(pairing, include_wine=True)


class UpdatePairingUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, pairing_id: int, request: UpdatePairingRequest) -> PairingResponse:
        pairing = self.pairing_service.update_pairing(
            user_id=user_id,
            pairing_id=pairing_id,
            food=request.food,
            effectiveness=request.effectiveness,
            notes=request.notes,
        )
        return _to_response(pairing, include_wine=True)


class DeletePairingUseCase:
    def __init__(self, pairing_service: PairingService):
        self.pairing_service = pairing_service

    def execute(self, user_id: int, pairing_id: int) -> bool:
        return self.pairing_service.remove_pairing(user_id, pairing_id)


def _to_response(pairing, include_wine: bool = False) -> PairingResponse:
    wine = None
    if include_wine and pairing.wine:
        wine_data = pairing.wine
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

    return PairingResponse(
        id=pairing.id,
        user_id=pairing.user_id,
        wine_id=pairing.wine_id,
        food=pairing.food,
        effectiveness=pairing.effectiveness,
        notes=pairing.notes,
        created_at=pairing.created_at,
        updated_at=pairing.updated_at,
        wine=wine,
    )
