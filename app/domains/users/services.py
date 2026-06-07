from typing import List, Optional

from ...core.security import hash_password, verify_password
from .domain import User, Email, Username, UserAlreadyExistsException, UserNotFoundException
from .repository import UserRepository

class UserService:
    """User domain service - contains business logic for user operations"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, email: str, username: str, password: str, full_name: Optional[str] = None) -> User:
        """Create a new user with business rules"""
        # Create value objects
        email_vo = Email(email)
        username_vo = Username(username)
        
        # Check business rules
        if self.user_repository.exists_by_email(email_vo):
            raise UserAlreadyExistsException(f"User with email {email} already exists")
        
        if self.user_repository.exists_by_username(username_vo):
            raise UserAlreadyExistsException(f"User with username {username} already exists")
        
        # Create domain entity
        user = User(
            email=email_vo,
            username=username_vo,
            password=hash_password(password),
            full_name=full_name
        )
        
        # Save to repository
        return self.user_repository.create(user)
    
    def authenticate(self, email: str, password: str) -> User:
        """Authenticate a user by email and password"""
        user = self.user_repository.get_by_email(Email(email))
        if not user or not verify_password(password, user.password):
            raise UserNotFoundException("Invalid email or password")
        if not user.can_login():
            raise UserNotFoundException("User account is inactive")
        return user

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.user_repository.get_all(skip=skip, limit=limit)
    
    def update_user(self, user_id: int, full_name: Optional[str] = None, password: Optional[str] = None, is_active: Optional[bool] = None) -> User:
        """Update user with business logic"""
        user = self.get_user_by_id(user_id)
        
        if full_name is not None or password is not None:
            hashed_password = hash_password(password) if password is not None else None
            user.update_profile(full_name=full_name, password=hashed_password)
        
        if is_active is not None:
            if is_active:
                user.activate()
            else:
                user.deactivate()
        
        return self.user_repository.update(user)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        user = self.get_user_by_id(user_id)
        return self.user_repository.delete(user_id)
    
    def activate_user(self, user_id: int) -> User:
        """Activate user"""
        user = self.get_user_by_id(user_id)
        user.activate()
        return self.user_repository.update(user)
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate user"""
        user = self.get_user_by_id(user_id)
        user.deactivate()
        return self.user_repository.update(user) 