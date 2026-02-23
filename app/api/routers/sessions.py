from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas import LearningSessionCreate, LearningSessionRead, LearningSessionUpdate, StatusMessage
from app.business.sessions_service import LearningSessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])
service = LearningSessionService()


@router.post("", response_model=LearningSessionRead, status_code=status.HTTP_201_CREATED)
def create_session(payload: LearningSessionCreate):
    session_id = service.create_session(
        payload.user_id,
        payload.topic_id,
        payload.session_date,
        payload.duration_minutes,
        payload.notes,
    )
    return service.get_session_by_id(session_id)


@router.get("", response_model=List[LearningSessionRead])
def list_sessions(
    user_id: Optional[UUID] = Query(default=None),
    topic_id: Optional[UUID] = Query(default=None),
):
    if (user_id is None and topic_id is None) or (user_id is not None and topic_id is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide exactly one of user_id or topic_id.",
        )
    if user_id is not None:
        return service.list_sessions_by_user(user_id)
    return service.list_sessions_by_topic(topic_id)


@router.get("/{session_id}", response_model=LearningSessionRead)
def get_session(session_id: UUID):
    return service.get_session_by_id(session_id)


@router.put("/{session_id}", response_model=LearningSessionRead)
def update_session(session_id: UUID, payload: LearningSessionUpdate):
    service.update_session(
        session_id,
        payload.session_date,
        payload.duration_minutes,
        payload.notes,
    )
    return service.get_session_by_id(session_id)


@router.delete("/{session_id}", response_model=StatusMessage)
def delete_session(session_id: UUID):
    service.delete_session(session_id)
    return StatusMessage(message="Learning session deleted.")

