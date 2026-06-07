from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ...domains.cellar.domain import CellarEntry
from ...domains.cellar.repository import CellarRepository
from ...domains.wines.domain import Wine
from ..database.models import CellarEntryModel


class SQLAlchemyCellarRepository(CellarRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, entry: CellarEntry) -> CellarEntry:
        db_entry = CellarEntryModel(
            user_id=entry.user_id,
            wine_id=entry.wine_id,
            quantity=entry.quantity,
            notes=entry.notes,
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return self.get_by_id(db_entry.id)

    def get_by_id(self, entry_id: int) -> Optional[CellarEntry]:
        db_entry = (
            self.db.query(CellarEntryModel)
            .options(joinedload(CellarEntryModel.wine))
            .filter(CellarEntryModel.id == entry_id)
            .first()
        )
        return self._to_domain(db_entry) if db_entry else None

    def get_by_user_and_wine(self, user_id: int, wine_id: int) -> Optional[CellarEntry]:
        db_entry = (
            self.db.query(CellarEntryModel)
            .filter(
                CellarEntryModel.user_id == user_id,
                CellarEntryModel.wine_id == wine_id,
            )
            .first()
        )
        return self._to_domain(db_entry) if db_entry else None

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CellarEntry]:
        db_entries = (
            self.db.query(CellarEntryModel)
            .options(joinedload(CellarEntryModel.wine))
            .filter(CellarEntryModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(entry) for entry in db_entries]

    def update(self, entry: CellarEntry) -> CellarEntry:
        db_entry = self.db.query(CellarEntryModel).filter(CellarEntryModel.id == entry.id).first()
        if not db_entry:
            return entry

        db_entry.quantity = entry.quantity
        db_entry.notes = entry.notes
        db_entry.updated_at = entry.updated_at
        self.db.commit()
        self.db.refresh(db_entry)
        return self._to_domain(db_entry)

    def delete(self, entry_id: int) -> bool:
        db_entry = self.db.query(CellarEntryModel).filter(CellarEntryModel.id == entry_id).first()
        if not db_entry:
            return False
        self.db.delete(db_entry)
        self.db.commit()
        return True

    def _to_domain(self, db_entry: CellarEntryModel) -> CellarEntry:
        wine = None
        if db_entry.wine:
            wine = Wine(
                id=db_entry.wine.id,
                name=db_entry.wine.name,
                year=db_entry.wine.year,
                grape=db_entry.wine.grape,
                country=db_entry.wine.country,
                region=db_entry.wine.region,
                color=db_entry.wine.color,
                description=db_entry.wine.description,
                created_at=db_entry.wine.created_at,
                updated_at=db_entry.wine.updated_at,
            )

        return CellarEntry(
            id=db_entry.id,
            user_id=db_entry.user_id,
            wine_id=db_entry.wine_id,
            quantity=db_entry.quantity,
            notes=db_entry.notes,
            created_at=db_entry.created_at,
            updated_at=db_entry.updated_at,
            wine=wine,
        )
