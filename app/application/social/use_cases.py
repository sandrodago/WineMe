from typing import List

from ...domains.social.domain import SocialConnectionNotFoundException
from ...domains.social.services import SocialService
from .dto import SendConnectionRequest, SocialConnectionResponse


class SendConnectionRequestUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int, request: SendConnectionRequest) -> SocialConnectionResponse:
        connection = self.social_service.send_request(user_id, request.addressee_id)
        return self._to_response(connection)

    def _to_response(self, connection) -> SocialConnectionResponse:
        return SocialConnectionResponse(
            id=connection.id,
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )


class AcceptConnectionUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int, connection_id: int) -> SocialConnectionResponse:
        connection = self.social_service.accept_request(user_id, connection_id)
        return self._to_response(connection)

    def _to_response(self, connection) -> SocialConnectionResponse:
        return SocialConnectionResponse(
            id=connection.id,
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )


class RejectConnectionUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int, connection_id: int) -> SocialConnectionResponse:
        connection = self.social_service.reject_request(user_id, connection_id)
        return self._to_response(connection)

    def _to_response(self, connection) -> SocialConnectionResponse:
        return SocialConnectionResponse(
            id=connection.id,
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )


class GetReceivedConnectionsUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int) -> List[SocialConnectionResponse]:
        return [self._to_response(connection) for connection in self.social_service.list_received_requests(user_id)]

    def _to_response(self, connection) -> SocialConnectionResponse:
        return SocialConnectionResponse(
            id=connection.id,
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )


class GetSentConnectionsUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int) -> List[SocialConnectionResponse]:
        return [self._to_response(connection) for connection in self.social_service.list_sent_requests(user_id)]

    def _to_response(self, connection) -> SocialConnectionResponse:
        return SocialConnectionResponse(
            id=connection.id,
            requester_id=connection.requester_id,
            addressee_id=connection.addressee_id,
            status=connection.status,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )


class DeleteConnectionUseCase:
    def __init__(self, social_service: SocialService):
        self.social_service = social_service

    def execute(self, user_id: int, connection_id: int) -> bool:
        return self.social_service.delete_connection(user_id, connection_id)
