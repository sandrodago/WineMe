from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Wine:
    """Wine domain entity"""
    id: int
    name: str
    year: int
    grape: str
    country: str
    region: str
    color: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow()
