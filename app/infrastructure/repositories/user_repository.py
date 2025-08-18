from sqlalchemy.orm import Session
from typing import List, Optional
from ...domains.users.repository import UserRepository
from ...domains.users.domain import User, Email, Username
from ..database.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            email=user.email.value,
            username=user.username.value,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Convert back to domain entity
        return self._to_domain_entity(db_user)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain_entity(db_user) if db_user else None
    
    def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email"""
        db_user = self.db.query(UserModel).filter(UserModel.email == email.value).first()
        return self._to_domain_entity(db_user) if db_user else None
    
    def get_by_username(self, username: Username) -> Optional[User]:
        """Get user by username"""
        db_user = self.db.query(UserModel).filter(UserModel.username == username.value).first()
        return self._to_domain_entity(db_user) if db_user else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        db_users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_domain_entity(db_user) for db_user in db_users]
    
    def update(self, user: User) -> User:
        """Update user"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            # Update the SQLAlchemy model attributes
            db_user.email = user.email.value
            db_user.username = user.username.value
            db_user.full_name = user.full_name
            db_user.is_active = user.is_active
            db_user.updated_at = user.updated_at
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_domain_entity(db_user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
    
    def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        return self.db.query(UserModel).filter(UserModel.email == email.value).first() is not None
    
    def exists_by_username(self, username: Username) -> bool:
        """Check if user exists by username"""
        return self.db.query(UserModel).filter(UserModel.username == username.value).first() is not None
    
    def _to_domain_entity(self, db_user: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        return User(
            id=db_user.id,
            email=Email(db_user.email),
            username=Username(db_user.username),
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        ) 