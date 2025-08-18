from typing import List, Optional
from ...domains.users.services import UserService
from ...domains.users.domain import UserAlreadyExistsException, UserNotFoundException
from .dto import CreateUserRequest, UpdateUserRequest, UserResponse

class CreateUserUseCase:
    """Use case for creating a user"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def execute(self, request: CreateUserRequest) -> UserResponse:
        """Execute the create user use case"""
        try:
            user = self.user_service.create_user(
                email=request.email,
                username=request.username,
                full_name=request.full_name
            )
            return self._to_response(user)
        except UserAlreadyExistsException as e:
            raise e
    
    def _to_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            display_name=user.display_name
        )

class GetUserUseCase:
    """Use case for getting a user by ID"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def execute(self, user_id: int) -> UserResponse:
        """Execute the get user use case"""
        try:
            user = self.user_service.get_user_by_id(user_id)
            return self._to_response(user)
        except UserNotFoundException as e:
            raise e
    
    def _to_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            display_name=user.display_name
        )

class GetUsersUseCase:
    """Use case for getting all users"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def execute(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Execute the get users use case"""
        users = self.user_service.get_all_users(skip=skip, limit=limit)
        return [self._to_response(user) for user in users]
    
    def _to_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            display_name=user.display_name
        )

class UpdateUserUseCase:
    """Use case for updating a user"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def execute(self, user_id: int, request: UpdateUserRequest) -> UserResponse:
        """Execute the update user use case"""
        try:
            user = self.user_service.update_user(
                user_id=user_id,
                full_name=request.full_name,
                is_active=request.is_active
            )
            return self._to_response(user)
        except UserNotFoundException as e:
            raise e
    
    def _to_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            display_name=user.display_name
        )

class DeleteUserUseCase:
    """Use case for deleting a user"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def execute(self, user_id: int) -> bool:
        """Execute the delete user use case"""
        try:
            return self.user_service.delete_user(user_id)
        except UserNotFoundException as e:
            raise e 