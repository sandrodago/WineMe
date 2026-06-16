from typing import List

from .domain import ACCEPTED, PENDING, REJECTED, SocialConnection, SocialConnectionNotFoundException
from .repository import SocialConnectionRepository


class SocialService:
    def __init__(self, social_repository: SocialConnectionRepository):
        self.social_repository = social_repository

    def send_request(self, requester_id: int, addressee_id: int) -> SocialConnection:
        existing = self.social_repository.get_between_users(requester_id, addressee_id)
        if existing and existing.status in {PENDING, ACCEPTED}:
            raise ValueError("A connection already exists between these users")
        if existing and existing.status == REJECTED:
            self.social_repository.delete(existing.id)

        connection = SocialConnection(requester_id=requester_id, addressee_id=addressee_id)
        return self.social_repository.create(connection)

    def accept_request(self, user_id: int, connection_id: int) -> SocialConnection:
        connection = self.social_repository.get_by_id(connection_id)
        if not connection or connection.addressee_id != user_id:
            raise SocialConnectionNotFoundException(f"Connection {connection_id} not found")
        connection.accept()
        return self.social_repository.update(connection)

    def reject_request(self, user_id: int, connection_id: int) -> SocialConnection:
        connection = self.social_repository.get_by_id(connection_id)
        if not connection or connection.addressee_id != user_id:
            raise SocialConnectionNotFoundException(f"Connection {connection_id} not found")
        connection.reject()
        return self.social_repository.update(connection)

    def list_received_requests(self, user_id: int) -> List[SocialConnection]:
        return self.social_repository.get_received_requests(user_id)

    def list_sent_requests(self, user_id: int) -> List[SocialConnection]:
        return self.social_repository.get_sent_requests(user_id)

    def get_friend_ids(self, user_id: int) -> List[int]:
        connections = self.social_repository.get_friends(user_id)
        friend_ids = []
        for connection in connections:
            friend_ids.append(
                connection.addressee_id if connection.requester_id == user_id else connection.requester_id
            )
        return friend_ids

    def delete_connection(self, user_id: int, connection_id: int) -> bool:
        connection = self.social_repository.get_by_id(connection_id)
        if not connection or (connection.requester_id != user_id and connection.addressee_id != user_id):
            raise SocialConnectionNotFoundException(f"Connection {connection_id} not found")
        return self.social_repository.delete(connection_id)
