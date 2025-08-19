from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import UserCreateRequest, UserUpdateRequest, UserResponse
from ....application.users.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)
from ....application.users.dto import CreateUserRequest as CreateUserDTO, UpdateUserRequest as UpdateUserDTO
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from ....domains.users.services import UserService

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get user service with repository"""
    user_repository = SQLAlchemyUserRepository(db)
    return UserService(user_repository)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_request: UserCreateRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    try:
        use_case = CreateUserUseCase(user_service)
        dto = CreateUserDTO(
            email=user_request.email,
            username=user_request.username,
            password=user_request.password,
            full_name=user_request.full_name
        )
        result = use_case.execute(dto)
        return UserResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """Get all users with pagination"""
    use_case = GetUsersUseCase(user_service)
    results = use_case.execute(skip=skip, limit=limit)
    return [UserResponse(**result.__dict__) for result in results]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by ID"""
    try:
        use_case = GetUserUseCase(user_service)
        result = use_case.execute(user_id)
        return UserResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_request: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Update a user"""
    try:
        use_case = UpdateUserUseCase(user_service)
        dto = UpdateUserDTO(
            full_name=user_request.full_name,
            password=user_request.password,
            is_active=user_request.is_active
        )
        result = use_case.execute(user_id, dto)
        return UserResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user"""
    try:
        use_case = DeleteUserUseCase(user_service)
        use_case.execute(user_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 