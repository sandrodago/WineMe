from sqlalchemy.orm import Session
from typing import List, Optional
from ...domains.wines.repository import WinesRepository
from ...domains.wines.domain import Wine
from ..database.models import WineModel

class SqlAlchemyWineRepository(WinesRepository):
    """SQLAlchemy implementation of WineRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, wine: Wine) -> Wine:
        """Create a new wine"""
        db_wine = WineModel(
            name=wine.name,
            year=wine.year,
            grape=wine.grape,
            country=wine.country,
            region=wine.region,
            color=wine.color,
            description=wine.description
        )
        self.db.add(db_wine)
        self.db.commit()
        self.db.refresh(db_wine)
        
        return self._to_domain(db_wine)
    
    def get_by_id(self, wine_id: int) -> Optional[Wine]:
        """Get wine by ID"""
        db_wine = self.db.query(WineModel).filter(WineModel.id == wine_id).first()
        return self._to_domain(db_wine) if db_wine else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get all wines with pagination"""
        db_wines = self.db.query(WineModel).offset(skip).limit(limit).all()
        return [self._to_domain(wine) for wine in db_wines]
    
    def get_by_name(self, name: str) -> Optional[Wine]:
        """Get wine by name"""
        db_wine = self.db.query(WineModel).filter(WineModel.name == name).first()
        return self._to_domain(db_wine) if db_wine else None
    
    def get_by_country(self, country: str, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get wines by country"""
        db_wines = self.db.query(WineModel).filter(WineModel.country == country).offset(skip).limit(limit).all()
        return [self._to_domain(wine) for wine in db_wines]
    
    def get_by_grape(self, grape: str, skip: int = 0, limit: int = 100) -> List[Wine]:
        """Get wines by grape variety"""
        db_wines = self.db.query(WineModel).filter(WineModel.grape == grape).offset(skip).limit(limit).all()
        return [self._to_domain(wine) for wine in db_wines]
    
    def update(self, wine: Wine) -> Wine:
        """Update wine"""
        db_wine = self.db.query(WineModel).filter(WineModel.id == wine.id).first()
        if not db_wine:
            raise ValueError(f"Wine with ID {wine.id} not found")
        
        db_wine.name = wine.name
        db_wine.year = wine.year
        db_wine.grape = wine.grape
        db_wine.country = wine.country
        db_wine.region = wine.region
        db_wine.color = wine.color
        db_wine.description = wine.description
        db_wine.updated_at = wine.updated_at
        
        self.db.commit()
        self.db.refresh(db_wine)
        
        return self._to_domain(db_wine)
    
    def delete(self, wine_id: int) -> bool:
        """Delete wine"""
        db_wine = self.db.query(WineModel).filter(WineModel.id == wine_id).first()
        if not db_wine:
            return False
        
        self.db.delete(db_wine)
        self.db.commit()
        return True
    
    def exists_by_name(self, name: str) -> bool:
        """Check if wine exists by name"""
        return self.db.query(WineModel).filter(WineModel.name == name).first() is not None
    
    def _to_domain(self, db_wine: WineModel) -> Wine:
        """Convert database model to domain entity"""
        return Wine(
            name=db_wine.name,
            year=db_wine.year,
            grape=db_wine.grape,
            country=db_wine.country,
            region=db_wine.region,
            color=db_wine.color,
            description=db_wine.description,
            id=db_wine.id,
            created_at=db_wine.created_at,
            updated_at=db_wine.updated_at
        )

