from typing import List, Optional

from ...domains.pairings.domain import WineMeMatch
from ...domains.pairings.services import PairingService
from ...domains.social.services import SocialService
from ...domains.tastings.services import TastingService
from ..wines.dto import WineResponse
from .dto import WineMeMatchResponse


class SearchWineMeUseCase:
    def __init__(
        self,
        pairing_service: PairingService,
        social_service: SocialService,
        tasting_service: TastingService,
    ):
        self.pairing_service = pairing_service
        self.social_service = social_service
        self.tasting_service = tasting_service

    def execute(self, user_id: int, food: str, skip: int = 0, limit: int = 100) -> List[WineMeMatchResponse]:
        friend_ids = self.social_service.get_friend_ids(user_id)
        pairings = self.pairing_service.get_wine_me_pairings(user_id, food, friend_ids=friend_ids)
        if not pairings:
            return []

        wine_ids = sorted({pairing.wine_id for pairing in pairings})
        tastings = self.tasting_service.get_tastings_for_wines(user_id, wine_ids)
        tasting_map = self._group_tastings(tastings)

        matches = self._aggregate(pairings, tasting_map)
        matches.sort(key=lambda item: (item.score or 0, item.latest_activity_at or item.latest_pairing_at, item.match_count), reverse=True)
        return [self._to_response(match) for match in matches[skip: skip + limit]]

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
            average_tasting_rating=match.average_tasting_rating,
            latest_tasting_at=match.latest_tasting_at,
            latest_tasting_rating=match.latest_tasting_rating,
            latest_notes=match.latest_notes,
            score=match.score,
        )

    def _group_tastings(self, tastings) -> dict[int, list]:
        grouped: dict[int, list] = {}
        for tasting in tastings:
            grouped.setdefault(tasting.wine_id, []).append(tasting)
        return grouped

    def _aggregate(self, pairings, tasting_map) -> List[WineMeMatch]:
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
                    "latest_tasting_at": None,
                    "latest_tasting_rating": None,
                    "average_tasting_rating": None,
                    "score": None,
                },
            )

            bucket["count"] += 1
            bucket["effectiveness_sum"] += pairing.effectiveness

            if pairing.created_at and pairing.created_at > bucket["latest_pairing_at"]:
                bucket["latest_pairing_at"] = pairing.created_at
                bucket["latest_food"] = pairing.food
                bucket["latest_effectiveness"] = pairing.effectiveness
                bucket["latest_notes"] = pairing.notes

        results = []
        for wine_id, data in grouped.items():
            tasting_bucket = tasting_map.get(wine_id, [])
            average_tasting_rating: Optional[float] = None
            latest_tasting_at = None
            latest_tasting_rating = None
            if tasting_bucket:
                average_tasting_rating = round(
                    sum(t.rating for t in tasting_bucket) / len(tasting_bucket), 2
                )
                latest_tasting = max(
                    tasting_bucket,
                    key=lambda t: t.created_at or data["latest_pairing_at"],
                )
                latest_tasting_at = latest_tasting.created_at
                latest_tasting_rating = latest_tasting.rating

            average_pairing_effectiveness = data["effectiveness_sum"] / data["count"]
            if average_tasting_rating is not None:
                score = round((average_tasting_rating * 0.7) + (average_pairing_effectiveness * 0.3), 2)
            else:
                score = round(average_pairing_effectiveness, 2)

            results.append(
                WineMeMatch(
                    wine=data["wine"],
                    match_count=data["count"],
                    average_effectiveness=round(average_pairing_effectiveness, 2),
                    latest_pairing_at=data["latest_pairing_at"],
                    latest_food=data["latest_food"],
                    latest_effectiveness=data["latest_effectiveness"],
                    latest_tasting_at=latest_tasting_at,
                    latest_tasting_rating=latest_tasting_rating,
                    average_tasting_rating=average_tasting_rating,
                    latest_notes=data["latest_notes"],
                    score=score,
                    latest_activity_at=max(
                        [d for d in [data["latest_pairing_at"], latest_tasting_at] if d is not None]
                    ),
                )
            )
        return results
