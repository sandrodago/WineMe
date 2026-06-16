from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ...domains.pairings.domain import Pairing
from ...domains.pairings.repository import PairingRepository
from ...domains.wines.domain import Wine
from ..database.models import PairingModel


class SQLAlchemyPairingRepository(PairingRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, pairing: Pairing) -> Pairing:
        db_pairing = PairingModel(
            user_id=pairing.user_id,
            wine_id=pairing.wine_id,
            food=pairing.food,
            effectiveness=pairing.effectiveness,
            notes=pairing.notes,
        )
        self.db.add(db_pairing)
        self.db.commit()
        self.db.refresh(db_pairing)
        return self.get_by_id(db_pairing.id)

    def get_by_id(self, pairing_id: int) -> Optional[Pairing]:
        db_pairing = (
            self.db.query(PairingModel)
            .options(joinedload(PairingModel.wine))
            .filter(PairingModel.id == pairing_id)
            .first()
        )
        return self._to_domain(db_pairing) if db_pairing else None

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Pairing]:
        db_pairings = (
            self.db.query(PairingModel)
            .options(joinedload(PairingModel.wine))
            .filter(PairingModel.user_id == user_id)
            .order_by(PairingModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(pairing) for pairing in db_pairings]

    def search_by_food(self, user_id: int, food: str, skip: int = 0, limit: Optional[int] = 100) -> List[Pairing]:
        pattern = f"%{food.strip().lower()}%"
        query = (
            self.db.query(PairingModel)
            .options(joinedload(PairingModel.wine))
            .filter(PairingModel.user_id == user_id)
            .filter(func.lower(PairingModel.food).like(pattern))
            .order_by(PairingModel.created_at.desc())
            .offset(skip)
        )
        if limit is not None:
            query = query.limit(limit)

        db_pairings = query.all()
        return [self._to_domain(pairing) for pairing in db_pairings]

    def update(self, pairing: Pairing) -> Pairing:
        db_pairing = self.db.query(PairingModel).filter(PairingModel.id == pairing.id).first()
        if not db_pairing:
            return pairing

        db_pairing.food = pairing.food
        db_pairing.effectiveness = pairing.effectiveness
        db_pairing.notes = pairing.notes
        db_pairing.updated_at = pairing.updated_at
        self.db.commit()
        self.db.refresh(db_pairing)
        return self._to_domain(db_pairing)

    def delete(self, pairing_id: int) -> bool:
        db_pairing = self.db.query(PairingModel).filter(PairingModel.id == pairing_id).first()
        if not db_pairing:
            return False
        self.db.delete(db_pairing)
        self.db.commit()
        return True

    def _to_domain(self, db_pairing: PairingModel) -> Pairing:
        wine = None
        if db_pairing.wine:
            wine = Wine(
                id=db_pairing.wine.id,
                name=db_pairing.wine.name,
                year=db_pairing.wine.year,
                grape=db_pairing.wine.grape,
                country=db_pairing.wine.country,
                region=db_pairing.wine.region,
                color=db_pairing.wine.color,
                description=db_pairing.wine.description,
                created_at=db_pairing.wine.created_at,
                updated_at=db_pairing.wine.updated_at,
            )

        return Pairing(
            id=db_pairing.id,
            user_id=db_pairing.user_id,
            wine_id=db_pairing.wine_id,
            food=db_pairing.food,
            effectiveness=db_pairing.effectiveness,
            notes=db_pairing.notes,
            created_at=db_pairing.created_at,
            updated_at=db_pairing.updated_at,
            wine=wine,
        )
