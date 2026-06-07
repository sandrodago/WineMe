from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....application.cellar.dto import AddToCellarRequest as AddToCellarDTO
from ....application.cellar.dto import UpdateCellarEntryRequest as UpdateCellarDTO
from ....application.cellar.use_cases import (
    AddToCellarUseCase,
    GetCellarEntryUseCase,
    GetCellarUseCase,
    RemoveFromCellarUseCase,
    UpdateCellarEntryUseCase,
)
from ....core.auth import get_current_user
from ....domains.cellar.domain import (
    CellarEntryAlreadyExistsException,
    CellarEntryNotFoundException,
)
from ....domains.cellar.services import CellarService
from ....domains.users.domain import User
from ....domains.wines.services import WineService
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.cellar_repository import SQLAlchemyCellarRepository
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ..schemas import CellarEntryCreateRequest, CellarEntryResponse, CellarEntryUpdateRequest

router = APIRouter()


def get_cellar_service(db: Session = Depends(get_db)) -> CellarService:
    wine_repository = SqlAlchemyWineRepository(db)
    wine_service = WineService(wine_repository)
    cellar_repository = SQLAlchemyCellarRepository(db)
    return CellarService(cellar_repository, wine_service)


def _to_schema(response) -> CellarEntryResponse:
    data = response.__dict__.copy()
    if data.get("wine"):
        data["wine"] = data["wine"].__dict__
    return CellarEntryResponse(**data)


@router.get("/", response_model=List[CellarEntryResponse])
def get_my_cellar(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    cellar_service: CellarService = Depends(get_cellar_service),
):
    use_case = GetCellarUseCase(cellar_service)
    results = use_case.execute(current_user.id, skip=skip, limit=limit)
    return [_to_schema(result) for result in results]


@router.post("/", response_model=CellarEntryResponse, status_code=status.HTTP_201_CREATED)
def add_to_cellar(
    request: CellarEntryCreateRequest,
    current_user: User = Depends(get_current_user),
    cellar_service: CellarService = Depends(get_cellar_service),
):
    try:
        use_case = AddToCellarUseCase(cellar_service)
        dto = AddToCellarDTO(
            wine_id=request.wine_id,
            quantity=request.quantity,
            notes=request.notes,
        )
        return _to_schema(use_case.execute(current_user.id, dto))
    except CellarEntryAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{entry_id}", response_model=CellarEntryResponse)
def get_cellar_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    cellar_service: CellarService = Depends(get_cellar_service),
):
    try:
        use_case = GetCellarEntryUseCase(cellar_service)
        return _to_schema(use_case.execute(current_user.id, entry_id))
    except CellarEntryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{entry_id}", response_model=CellarEntryResponse)
def update_cellar_entry(
    entry_id: int,
    request: CellarEntryUpdateRequest,
    current_user: User = Depends(get_current_user),
    cellar_service: CellarService = Depends(get_cellar_service),
):
    try:
        use_case = UpdateCellarEntryUseCase(cellar_service)
        dto = UpdateCellarDTO(quantity=request.quantity, notes=request.notes)
        return _to_schema(use_case.execute(current_user.id, entry_id, dto))
    except CellarEntryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cellar(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    cellar_service: CellarService = Depends(get_cellar_service),
):
    try:
        use_case = RemoveFromCellarUseCase(cellar_service)
        use_case.execute(current_user.id, entry_id)
        return None
    except CellarEntryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
