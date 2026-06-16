from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ....application.wine_me.use_cases import SearchWineMeUseCase
from ....core.auth import get_current_user
from ....domains.pairings.services import PairingService
from ....domains.social.services import SocialService
from ....domains.users.domain import User
from ....domains.wines.services import WineService
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.pairing_repository import SQLAlchemyPairingRepository
from ....infrastructure.repositories.social_repository import SQLAlchemySocialConnectionRepository
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ..schemas import WineMeMatchResponse

router = APIRouter()


def get_pairing_service(db: Session = Depends(get_db)) -> PairingService:
    wine_repository = SqlAlchemyWineRepository(db)
    wine_service = WineService(wine_repository)
    pairing_repository = SQLAlchemyPairingRepository(db)
    return PairingService(pairing_repository, wine_service)


def get_social_service(db: Session = Depends(get_db)) -> SocialService:
    social_repository = SQLAlchemySocialConnectionRepository(db)
    return SocialService(social_repository)


def _to_schema(response) -> WineMeMatchResponse:
    data = response.__dict__.copy()
    data["wine"] = data["wine"].__dict__
    return WineMeMatchResponse(**data)


@router.get("/wine-me", response_model=List[WineMeMatchResponse])
def wine_me(
    food: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
    social_service: SocialService = Depends(get_social_service),
):
    use_case = SearchWineMeUseCase(pairing_service, social_service)
    results = use_case.execute(current_user.id, food=food, skip=skip, limit=limit)
    return [_to_schema(result) for result in results]
