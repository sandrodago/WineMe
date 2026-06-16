from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....application.social.dto import SendConnectionRequest
from ....application.social.use_cases import (
    AcceptConnectionUseCase,
    DeleteConnectionUseCase,
    GetReceivedConnectionsUseCase,
    GetSentConnectionsUseCase,
    RejectConnectionUseCase,
    SendConnectionRequestUseCase,
)
from ....core.auth import get_current_user
from ....domains.social.domain import SocialConnectionNotFoundException
from ....domains.social.services import SocialService
from ....domains.users.domain import User
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.social_repository import SQLAlchemySocialConnectionRepository
from ..schemas import SocialConnectionCreateRequest, SocialConnectionResponse

router = APIRouter()


def get_social_service(db: Session = Depends(get_db)) -> SocialService:
    social_repository = SQLAlchemySocialConnectionRepository(db)
    return SocialService(social_repository)


def _to_schema(response) -> SocialConnectionResponse:
    return SocialConnectionResponse(**response.__dict__)


@router.post("/requests", response_model=SocialConnectionResponse, status_code=status.HTTP_201_CREATED)
def send_request(
    request: SocialConnectionCreateRequest,
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    try:
        use_case = SendConnectionRequestUseCase(social_service)
        result = use_case.execute(current_user.id, SendConnectionRequest(addressee_id=request.addressee_id))
        return _to_schema(result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/requests/incoming", response_model=List[SocialConnectionResponse])
def incoming_requests(
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    use_case = GetReceivedConnectionsUseCase(social_service)
    return [_to_schema(result) for result in use_case.execute(current_user.id)]


@router.get("/requests/outgoing", response_model=List[SocialConnectionResponse])
def outgoing_requests(
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    use_case = GetSentConnectionsUseCase(social_service)
    return [_to_schema(result) for result in use_case.execute(current_user.id)]


@router.post("/requests/{connection_id}/accept", response_model=SocialConnectionResponse)
def accept_request(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    try:
        use_case = AcceptConnectionUseCase(social_service)
        return _to_schema(use_case.execute(current_user.id, connection_id))
    except SocialConnectionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/requests/{connection_id}/reject", response_model=SocialConnectionResponse)
def reject_request(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    try:
        use_case = RejectConnectionUseCase(social_service)
        return _to_schema(use_case.execute(current_user.id, connection_id))
    except SocialConnectionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    social_service: SocialService = Depends(get_social_service),
):
    try:
        use_case = DeleteConnectionUseCase(social_service)
        use_case.execute(current_user.id, connection_id)
        return None
    except SocialConnectionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

