from ...domains.users.domain import UserNotFoundException
from ...domains.users.services import UserService
from ..users.dto import UserResponse
from ..users.use_cases import CreateUserUseCase
from ...core.security import create_access_token


class RegisterUseCase:
    def __init__(self, user_service: UserService):
        self.create_user = CreateUserUseCase(user_service)

    def execute(self, request) -> tuple[UserResponse, str]:
        user = self.create_user.execute(request)
        token = create_access_token(str(user.id))
        return user, token


class LoginUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, email: str, password: str) -> tuple[UserResponse, str]:
        try:
            user = self.user_service.authenticate(email, password)
        except UserNotFoundException as e:
            raise e

        token = create_access_token(str(user.id))
        response = UserResponse(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            display_name=user.display_name,
        )
        return response, token
