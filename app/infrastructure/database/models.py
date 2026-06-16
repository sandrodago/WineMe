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
    sent_connection_requests = relationship("SocialConnectionModel", foreign_keys="SocialConnectionModel.requester_id", back_populates="requester")
    received_connection_requests = relationship("SocialConnectionModel", foreign_keys="SocialConnectionModel.addressee_id", back_populates="addressee")

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
    tastings = relationship("TastingModel", back_populates="wine")
    pairings = relationship("PairingModel", back_populates="wine")


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


class TastingModel(Base):
    """A user's tasting note and rating for a wine"""
    __tablename__ = "tastings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("UserModel", backref="tastings")
    wine = relationship("WineModel", back_populates="tastings")


class PairingModel(Base):
    """A user's food and wine pairing note"""
    __tablename__ = "pairings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False, index=True)
    food = Column(String, nullable=False, index=True)
    effectiveness = Column(Integer, nullable=False, default=3)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("UserModel", backref="pairings")
    wine = relationship("WineModel", back_populates="pairings")


class SocialConnectionModel(Base):
    """Friend request / connection between two users"""
    __tablename__ = "social_connections"
    __table_args__ = (UniqueConstraint("requester_id", "addressee_id", name="uq_social_connection_pair"),)

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    requester = relationship("UserModel", foreign_keys=[requester_id], back_populates="sent_connection_requests")
    addressee = relationship("UserModel", foreign_keys=[addressee_id], back_populates="received_connection_requests")
