from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....application.tastings.dto import AddTastingRequest as AddTastingDTO
from ....application.tastings.dto import UpdateTastingRequest as UpdateTastingDTO
from ....application.tastings.use_cases import (
    AddTastingUseCase,
    DeleteTastingUseCase,
    GetTastingUseCase,
    GetTastingsUseCase,
    UpdateTastingUseCase,
)
from ....core.auth import get_current_user
from ....domains.tastings.domain import TastingNotFoundException
from ....domains.tastings.services import TastingService
from ....domains.users.domain import User
from ....domains.wines.services import WineService
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.tasting_repository import SQLAlchemyTastingRepository
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ..schemas import TastingCreateRequest, TastingResponse, TastingUpdateRequest

router = APIRouter()


def get_tasting_service(db: Session = Depends(get_db)) -> TastingService:
    wine_repository = SqlAlchemyWineRepository(db)
    wine_service = WineService(wine_repository)
    tasting_repository = SQLAlchemyTastingRepository(db)
    return TastingService(tasting_repository, wine_service)


def _to_schema(response) -> TastingResponse:
    data = response.__dict__.copy()
    if data.get("wine"):
        data["wine"] = data["wine"].__dict__
    return TastingResponse(**data)


@router.get("/", response_model=List[TastingResponse])
def get_my_tastings(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    tasting_service: TastingService = Depends(get_tasting_service),
):
    use_case = GetTastingsUseCase(tasting_service)
    results = use_case.execute(current_user.id, skip=skip, limit=limit)
    return [_to_schema(result) for result in results]


@router.post("/", response_model=TastingResponse, status_code=status.HTTP_201_CREATED)
def add_tasting(
    request: TastingCreateRequest,
    current_user: User = Depends(get_current_user),
    tasting_service: TastingService = Depends(get_tasting_service),
):
    try:
        use_case = AddTastingUseCase(tasting_service)
        dto = AddTastingDTO(
            wine_id=request.wine_id,
            rating=request.rating,
            notes=request.notes,
        )
        return _to_schema(use_case.execute(current_user.id, dto))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{tasting_id}", response_model=TastingResponse)
def get_tasting(
    tasting_id: int,
    current_user: User = Depends(get_current_user),
    tasting_service: TastingService = Depends(get_tasting_service),
):
    try:
        use_case = GetTastingUseCase(tasting_service)
        return _to_schema(use_case.execute(current_user.id, tasting_id))
    except TastingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{tasting_id}", response_model=TastingResponse)
def update_tasting(
    tasting_id: int,
    request: TastingUpdateRequest,
    current_user: User = Depends(get_current_user),
    tasting_service: TastingService = Depends(get_tasting_service),
):
    try:
        use_case = UpdateTastingUseCase(tasting_service)
        dto = UpdateTastingDTO(rating=request.rating, notes=request.notes)
        return _to_schema(use_case.execute(current_user.id, tasting_id, dto))
    except TastingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{tasting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasting(
    tasting_id: int,
    current_user: User = Depends(get_current_user),
    tasting_service: TastingService = Depends(get_tasting_service),
):
    try:
        use_case = DeleteTastingUseCase(tasting_service)
        use_case.execute(current_user.id, tasting_id)
        return None
    except TastingNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

