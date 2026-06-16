from dataclasses import dataclass
from datetime import datetime
from typing import Optional


PENDING = "pending"
ACCEPTED = "accepted"
REJECTED = "rejected"


@dataclass
class SocialConnection:
    requester_id: int
    addressee_id: int
    status: str = PENDING
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.requester_id == self.addressee_id:
            raise ValueError("You cannot connect with yourself")
        if self.status not in {PENDING, ACCEPTED, REJECTED}:
            raise ValueError("Invalid connection status")
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def accept(self) -> None:
        self.status = ACCEPTED
        self.updated_at = datetime.utcnow()

    def reject(self) -> None:
        self.status = REJECTED
        self.updated_at = datetime.utcnow()


class SocialConnectionNotFoundException(Exception):
    pass

