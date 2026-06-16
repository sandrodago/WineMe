from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ....application.auth.use_cases import LoginUseCase, RegisterUseCase
from ....application.users.dto import CreateUserRequest as CreateUserDTO
from ....core.auth import get_current_user, get_user_service
from ....domains.users.domain import User, UserAlreadyExistsException, UserNotFoundException
from ....domains.users.services import UserService
from ..schemas import AuthResponse, UserCreateRequest, UserResponse

router = APIRouter()


def _to_user_response(user) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email.value,
        username=user.username.value,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        display_name=user.display_name,
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_request: UserCreateRequest,
    user_service: UserService = Depends(get_user_service),
):
    try:
        use_case = RegisterUseCase(user_service)
        dto = CreateUserDTO(
            email=user_request.email,
            username=user_request.username,
            password=user_request.password,
            full_name=user_request.full_name,
        )
        user, token = use_case.execute(dto)
        return AuthResponse(access_token=token, user=_to_user_response(user))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AuthResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    try:
        use_case = LoginUseCase(user_service)
        user, token = use_case.execute(form_data.username, form_data.password)
        return AuthResponse(access_token=token, user=_to_user_response(user))
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email.value,
        username=current_user.username.value,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        display_name=current_user.display_name,
    )
