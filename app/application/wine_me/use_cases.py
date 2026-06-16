from typing import List

from ...domains.pairings.services import PairingService
from ...domains.social.services import SocialService
from ..wines.dto import WineResponse
from .dto import WineMeMatchResponse


class SearchWineMeUseCase:
    def __init__(self, pairing_service: PairingService, social_service: SocialService):
        self.pairing_service = pairing_service
        self.social_service = social_service

    def execute(self, user_id: int, food: str, skip: int = 0, limit: int = 100) -> List[WineMeMatchResponse]:
        friend_ids = self.social_service.get_friend_ids(user_id)
        matches = self.pairing_service.search_wine_me(
            user_id,
            food,
            friend_ids=friend_ids,
            skip=skip,
            limit=limit,
        )
        return [self._to_response(match) for match in matches]

    def _to_response(self, match) -> WineMeMatchResponse:
        wine = match.wine
        wine_response = WineResponse(
            id=wine.id,
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description,
            created_at=wine.created_at,
            updated_at=wine.updated_at,
        )
        return WineMeMatchResponse(
            wine=wine_response,
            match_count=match.match_count,
            average_effectiveness=match.average_effectiveness,
            latest_pairing_at=match.latest_pairing_at,
            latest_food=match.latest_food,
            latest_effectiveness=match.latest_effectiveness,
            latest_notes=match.latest_notes,
        )
