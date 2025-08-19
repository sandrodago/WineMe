from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import WineCreateRequest, WineUpdateRequest, WineResponse
from ....application.wines.use_cases import (
    CreateWineUseCase,
    GetWineUseCase,
    GetWinesUseCase,
    UpdateWineUseCase,
    DeleteWineUseCase
)
from ....application.wines.dto import CreateWineRequest as CreateWineDTO, UpdateWineRequest as UpdateWineDTO
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.wine_repository import SqlAlchemyWineRepository
from ....domains.wines.services import WineService

router = APIRouter()

def get_wine_service(db: Session = Depends(get_db)) -> WineService:
    """Dependency to get wine service with repository"""
    wine_repository = SqlAlchemyWineRepository(db)
    return WineService(wine_repository)

@router.post("/", response_model=WineResponse, status_code=status.HTTP_201_CREATED)
def create_wine(
    wine_request: WineCreateRequest,
    wine_service: WineService = Depends(get_wine_service)
):
    """Create a new wine"""
    try:
        use_case = CreateWineUseCase(wine_service)
        dto = CreateWineDTO(
            name=wine_request.name,
            year=wine_request.year,
            grape=wine_request.grape,
            country=wine_request.country,
            region=wine_request.region,
            color=wine_request.color,
            description=wine_request.description
        )
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{wine_id}", response_model=WineResponse)
def get_wine(
    wine_id: int,
    wine_service: WineService = Depends(get_wine_service)
):
    """Get a wine by ID"""
    try:
        use_case = GetWineUseCase(wine_service)
        return use_case.execute(wine_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/", response_model=List[WineResponse])
def get_wines(
    skip: int = 0,
    limit: int = 100,
    wine_service: WineService = Depends(get_wine_service)
):
    """Get all wines"""
    use_case = GetWinesUseCase(wine_service)
    return use_case.execute(skip=skip, limit=limit)

@router.put("/{wine_id}", response_model=WineResponse)
def update_wine(
    wine_id: int,
    wine_request: WineUpdateRequest,
    wine_service: WineService = Depends(get_wine_service)
):
    """Update a wine"""
    try:
        use_case = UpdateWineUseCase(wine_service)
        dto = UpdateWineDTO(
            name=wine_request.name,
            year=wine_request.year,
            grape=wine_request.grape,
            country=wine_request.country,
            region=wine_request.region,
            color=wine_request.color,
            description=wine_request.description
        )
        return use_case.execute(wine_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{wine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wine(
    wine_id: int,
    wine_service: WineService = Depends(get_wine_service)
):
    """Delete a wine"""
    try:
        use_case = DeleteWineUseCase(wine_service)
        success = use_case.execute(wine_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wine not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
