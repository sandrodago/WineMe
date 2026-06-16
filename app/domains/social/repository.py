from abc import ABC, abstractmethod
from typing import List, Optional

from .domain import SocialConnection


class SocialConnectionRepository(ABC):
    @abstractmethod
    def create(self, connection: SocialConnection) -> SocialConnection:
        pass

    @abstractmethod
    def get_by_id(self, connection_id: int) -> Optional[SocialConnection]:
        pass

    @abstractmethod
    def get_between_users(self, user_a_id: int, user_b_id: int) -> Optional[SocialConnection]:
        pass

    @abstractmethod
    def get_received_requests(self, user_id: int) -> List[SocialConnection]:
        pass

    @abstractmethod
    def get_sent_requests(self, user_id: int) -> List[SocialConnection]:
        pass

    @abstractmethod
    def get_friends(self, user_id: int) -> List[SocialConnection]:
        pass

    @abstractmethod
    def update(self, connection: SocialConnection) -> SocialConnection:
        pass

    @abstractmethod
    def delete(self, connection_id: int) -> bool:
        pass

