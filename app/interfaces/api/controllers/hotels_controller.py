from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.application.hotels.use_cases import (
    CreateHotelUseCase, GetHotelUseCase, UpdateHotelUseCase, 
    DeleteHotelUseCase, ListHotelsUseCase, SearchHotelsUseCase
)
from app.application.hotels.dto import HotelCreateDTO, HotelUpdateDTO, HotelResponseDTO
from app.interfaces.api.schemas import HotelCreate, HotelUpdate, HotelResponse
from app.core.container import get_hotel_domain_service, get_session

router = APIRouter(prefix="/hotels", tags=["hotels"])

@router.post("/", response_model=HotelResponse, status_code=201)
async def create_hotel(
    hotel_data: HotelCreate,
    session: Session = Depends(get_session)
):
    """Create a new hotel"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        create_use_case = CreateHotelUseCase(hotel_domain_service)
        
        dto = HotelCreateDTO(name=hotel_data.name, city=hotel_data.city)
        result = await create_use_case.execute(dto)
        
        return HotelResponse(
            id=result.id,
            name=result.name,
            city=result.city,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(
    hotel_id: int,
    session: Session = Depends(get_session)
):
    """Get a hotel by ID"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        get_use_case = GetHotelUseCase(hotel_domain_service)
        
        result = await get_use_case.execute(hotel_id)
        
        return HotelResponse(
            id=result.id,
            name=result.name,
            city=result.city,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.put("/{hotel_id}", response_model=HotelResponse)
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelUpdate,
    session: Session = Depends(get_session)
):
    """Update a hotel"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        update_use_case = UpdateHotelUseCase(hotel_domain_service)
        
        dto = HotelUpdateDTO(name=hotel_data.name, city=hotel_data.city)
        result = await update_use_case.execute(hotel_id, dto)
        
        return HotelResponse(
            id=result.id,
            name=result.name,
            city=result.city,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(
    hotel_id: int,
    session: Session = Depends(get_session)
):
    """Delete a hotel"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        delete_use_case = DeleteHotelUseCase(hotel_domain_service)
        
        await delete_use_case.execute(hotel_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hotel not found")

@router.get("/", response_model=List[HotelResponse])
async def list_hotels(
    city: Optional[str] = Query(None, description="Filter by city"),
    session: Session = Depends(get_session)
):
    """List all hotels with optional city filter"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        list_use_case = ListHotelsUseCase(hotel_domain_service)
        
        results = await list_use_case.execute(city_filter=city)
        
        return [
            HotelResponse(
                id=result.id,
                name=result.name,
                city=result.city,
                created_at=result.created_at,
                updated_at=result.updated_at
            ) for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/", response_model=dict[str, List[HotelResponse]])  
async def search_hotels(
    name: Optional[str] = Query(None, description="Filter by name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    session: Session = Depends(get_session)
):
    """Search hotels by name and/or city"""
    try:
        hotel_domain_service = get_hotel_domain_service(session)
        search_use_case = SearchHotelsUseCase(hotel_domain_service)
        
        results = await search_use_case.execute(name_filter=name, city_filter=city)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error 2") 