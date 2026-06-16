from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SendConnectionRequest:
    addressee_id: int


@dataclass
class SocialConnectionResponse:
    id: int
    requester_id: int
    addressee_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

