from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....application.pairings.dto import AddPairingRequest as AddPairingDTO
from ....application.pairings.dto import UpdatePairingRequest as UpdatePairingDTO
from ....application.pairings.use_cases import (
    AddPairingUseCase,
    DeletePairingUseCase,
    GetPairingUseCase,
    GetPairingsUseCase,
    UpdatePairingUseCase,
)
from ....core.auth import get_current_user
from ....domains.pairings.domain import PairingNotFoundException
from ....domains.pairings.services import PairingService
from ....domains.users.domain import User
from ....domains.wines.services import WineService
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.pairing_repository import SQLAlchemyPairingRepository
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ..schemas import PairingCreateRequest, PairingResponse, PairingUpdateRequest

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


@router.get("/", response_model=List[PairingResponse])
def get_my_pairings(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    use_case = GetPairingsUseCase(pairing_service)
    results = use_case.execute(current_user.id, skip=skip, limit=limit)
    return [_to_schema(result) for result in results]


@router.post("/", response_model=PairingResponse, status_code=status.HTTP_201_CREATED)
def add_pairing(
    request: PairingCreateRequest,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    try:
        use_case = AddPairingUseCase(pairing_service)
        dto = AddPairingDTO(
            wine_id=request.wine_id,
            food=request.food,
            effectiveness=request.effectiveness,
            notes=request.notes,
        )
        return _to_schema(use_case.execute(current_user.id, dto))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{pairing_id}", response_model=PairingResponse)
def get_pairing(
    pairing_id: int,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    try:
        use_case = GetPairingUseCase(pairing_service)
        return _to_schema(use_case.execute(current_user.id, pairing_id))
    except PairingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{pairing_id}", response_model=PairingResponse)
def update_pairing(
    pairing_id: int,
    request: PairingUpdateRequest,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    try:
        use_case = UpdatePairingUseCase(pairing_service)
        dto = UpdatePairingDTO(
            food=request.food,
            effectiveness=request.effectiveness,
            notes=request.notes,
        )
        return _to_schema(use_case.execute(current_user.id, pairing_id, dto))
    except PairingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{pairing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pairing(
    pairing_id: int,
    current_user: User = Depends(get_current_user),
    pairing_service: PairingService = Depends(get_pairing_service),
):
    try:
        use_case = DeletePairingUseCase(pairing_service)
        use_case.execute(current_user.id, pairing_id)
        return None
    except PairingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
