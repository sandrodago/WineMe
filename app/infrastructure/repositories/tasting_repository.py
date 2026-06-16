from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ...domains.tastings.domain import Tasting
from ...domains.tastings.repository import TastingRepository
from ...domains.wines.domain import Wine
from ..database.models import TastingModel


class SQLAlchemyTastingRepository(TastingRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, tasting: Tasting) -> Tasting:
        db_tasting = TastingModel(
            user_id=tasting.user_id,
            wine_id=tasting.wine_id,
            rating=tasting.rating,
            notes=tasting.notes,
        )
        self.db.add(db_tasting)
        self.db.commit()
        self.db.refresh(db_tasting)
        return self.get_by_id(db_tasting.id)

    def get_by_id(self, tasting_id: int) -> Optional[Tasting]:
        db_tasting = (
            self.db.query(TastingModel)
            .options(joinedload(TastingModel.wine))
            .filter(TastingModel.id == tasting_id)
            .first()
        )
        return self._to_domain(db_tasting) if db_tasting else None

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Tasting]:
        db_tastings = (
            self.db.query(TastingModel)
            .options(joinedload(TastingModel.wine))
            .filter(TastingModel.user_id == user_id)
            .order_by(TastingModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(tasting) for tasting in db_tastings]

    def get_by_user_and_wines(self, user_id: int, wine_ids: List[int]) -> List[Tasting]:
        if not wine_ids:
            return []

        db_tastings = (
            self.db.query(TastingModel)
            .options(joinedload(TastingModel.wine))
            .filter(TastingModel.user_id == user_id)
            .filter(TastingModel.wine_id.in_(wine_ids))
            .order_by(TastingModel.created_at.desc())
            .all()
        )
        return [self._to_domain(tasting) for tasting in db_tastings]

    def update(self, tasting: Tasting) -> Tasting:
        db_tasting = self.db.query(TastingModel).filter(TastingModel.id == tasting.id).first()
        if not db_tasting:
            return tasting

        db_tasting.rating = tasting.rating
        db_tasting.notes = tasting.notes
        db_tasting.updated_at = tasting.updated_at
        self.db.commit()
        self.db.refresh(db_tasting)
        return self._to_domain(db_tasting)

    def delete(self, tasting_id: int) -> bool:
        db_tasting = self.db.query(TastingModel).filter(TastingModel.id == tasting_id).first()
        if not db_tasting:
            return False
        self.db.delete(db_tasting)
        self.db.commit()
        return True

    def _to_domain(self, db_tasting: TastingModel) -> Tasting:
        wine = None
        if db_tasting.wine:
            wine = Wine(
                id=db_tasting.wine.id,
                name=db_tasting.wine.name,
                year=db_tasting.wine.year,
                grape=db_tasting.wine.grape,
                country=db_tasting.wine.country,
                region=db_tasting.wine.region,
                color=db_tasting.wine.color,
                description=db_tasting.wine.description,
                created_at=db_tasting.wine.created_at,
                updated_at=db_tasting.wine.updated_at,
            )

        return Tasting(
            id=db_tasting.id,
            user_id=db_tasting.user_id,
            wine_id=db_tasting.wine_id,
            rating=db_tasting.rating,
            notes=db_tasting.notes,
            created_at=db_tasting.created_at,
            updated_at=db_tasting.updated_at,
            wine=wine,
        )
