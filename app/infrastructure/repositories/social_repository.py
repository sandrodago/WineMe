from typing import List, Optional

from sqlalchemy.orm import Session

from ...domains.social.domain import SocialConnection
from ...domains.social.repository import SocialConnectionRepository
from ..database.models import SocialConnectionModel


class SQLAlchemySocialConnectionRepository(SocialConnectionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, connection: SocialConnection) -> SocialConnection:
        db_connection = SocialConnectionModel(
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
        )
        self.db.add(db_connection)
        self.db.commit()
        self.db.refresh(db_connection)
        return self._to_domain(db_connection)

    def get_by_id(self, connection_id: int) -> Optional[SocialConnection]:
        db_connection = self.db.query(SocialConnectionModel).filter(SocialConnectionModel.id == connection_id).first()
        return self._to_domain(db_connection) if db_connection else None

    def get_between_users(self, user_a_id: int, user_b_id: int) -> Optional[SocialConnection]:
        db_connection = (
            self.db.query(SocialConnectionModel)
            .filter(
                ((SocialConnectionModel.requester_id == user_a_id) & (SocialConnectionModel.addressee_id == user_b_id))
                | ((SocialConnectionModel.requester_id == user_b_id) & (SocialConnectionModel.addressee_id == user_a_id))
            )
            .first()
        )
        return self._to_domain(db_connection) if db_connection else None

    def get_received_requests(self, user_id: int) -> List[SocialConnection]:
        db_connections = (
            self.db.query(SocialConnectionModel)
            .filter(SocialConnectionModel.addressee_id == user_id)
            .filter(SocialConnectionModel.status == "pending")
            .all()
        )
        return [self._to_domain(connection) for connection in db_connections]

    def get_sent_requests(self, user_id: int) -> List[SocialConnection]:
        db_connections = (
            self.db.query(SocialConnectionModel)
            .filter(SocialConnectionModel.requester_id == user_id)
            .all()
        )
        return [self._to_domain(connection) for connection in db_connections]

    def get_friends(self, user_id: int) -> List[SocialConnection]:
        db_connections = (
            self.db.query(SocialConnectionModel)
            .filter(
                ((SocialConnectionModel.requester_id == user_id) | (SocialConnectionModel.addressee_id == user_id))
            )
            .filter(SocialConnectionModel.status == "accepted")
            .all()
        )
        return [self._to_domain(connection) for connection in db_connections]

    def update(self, connection: SocialConnection) -> SocialConnection:
        db_connection = self.db.query(SocialConnectionModel).filter(SocialConnectionModel.id == connection.id).first()
        if not db_connection:
            return connection

        db_connection.status = connection.status
        db_connection.updated_at = connection.updated_at
        self.db.commit()
        self.db.refresh(db_connection)
        return self._to_domain(db_connection)

    def delete(self, connection_id: int) -> bool:
        db_connection = self.db.query(SocialConnectionModel).filter(SocialConnectionModel.id == connection_id).first()
        if not db_connection:
            return False
        self.db.delete(db_connection)
        self.db.commit()
        return True

    def _to_domain(self, db_connection: SocialConnectionModel) -> SocialConnection:
        return SocialConnection(
            id=db_connection.id,
            requester_id=db_connection.requester_id,
            addressee_id=db_connection.addressee_id,
            status=db_connection.status,
            created_at=db_connection.created_at,
            updated_at=db_connection.updated_at,
        )

