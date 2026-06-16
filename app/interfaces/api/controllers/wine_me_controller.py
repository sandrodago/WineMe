from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ....application.pairings.use_cases import SearchPairingsUseCase
from ....core.auth import get_current_user
from ....domains.pairings.services import PairingService
from ....domains.users.domain import User
from ....domains.wines.services import WineService
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.pairing_repository import SQLAlchemyPairingRepository
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ..schemas import PairingResponse

router = APIRouter()


def get_pairing_service(db: Session = Depends(get_db)) -> PairingService:
    wine_repository = SqlAlchemyWineRepository(db)
    wine_service = WineService(wine_repository)
    pairing_repository = SQLAlchemyPairingRepository(db)
    return PairingService(pairing_repository, wine_service)


def _to_schema(response) -> PairingResponse:
    data = response.__dict__.copy()
    if data.get("wine"):
        data["wine"] = data["wine"].__dict__
    return PairingResponse(**data)


@router.get("/wine-me", response_model=List[PairingResponse])
def wine_me(
    food: str = Query(..., min_length=1),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    use_case = SearchPairingsUseCase(pairing_service)
    results = use_case.execute(current_user.id, food=food, skip=skip, limit=limit)
    return [_to_schema(result) for result in results]

