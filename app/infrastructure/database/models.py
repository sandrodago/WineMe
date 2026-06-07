from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    """SQLAlchemy model for User - Infrastructure concern"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WineModel(Base):
    """SQLAlchemy model for Wine - Infrastructure concern"""
    __tablename__ = "wines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    grape = Column(String, nullable=False)
    country = Column(String, nullable=False)
    region = Column(String, nullable=False)
    color = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    cellar_entries = relationship("CellarEntryModel", back_populates="wine")


class CellarEntryModel(Base):
    """A user's wine inventory entry"""
    __tablename__ = "cellar_entries"
    __table_args__ = (UniqueConstraint("user_id", "wine_id", name="uq_user_wine"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("UserModel", backref="cellar_entries")
    wine = relationship("WineModel", back_populates="cellar_entries")