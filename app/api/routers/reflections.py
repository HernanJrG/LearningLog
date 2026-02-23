from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas import ReflectionCreate, ReflectionRead, ReflectionUpdate, StatusMessage
from app.business.reflections_service import ReflectionService

router = APIRouter(prefix="/reflections", tags=["reflections"])
service = ReflectionService()


@router.post("", response_model=ReflectionRead, status_code=status.HTTP_201_CREATED)
def create_reflection(payload: ReflectionCreate):
    reflection_id = service.create_reflection(payload.session_id, payload.rating, payload.summary)
    return service.get_reflection_by_id(reflection_id)


@router.get("", response_model=List[ReflectionRead])
def list_reflections(
    session_id: Optional[UUID] = Query(default=None),
    topic_id: Optional[UUID] = Query(default=None),
):
    if (session_id is None and topic_id is None) or (session_id is not None and topic_id is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide exactly one of session_id or topic_id.",
        )
    if session_id is not None:
        return service.list_reflections_by_session(session_id)
    return service.list_reflections_by_topic(topic_id)


@router.get("/{reflection_id}", response_model=ReflectionRead)
def get_reflection(reflection_id: UUID):
    return service.get_reflection_by_id(reflection_id)


@router.put("/{reflection_id}", response_model=ReflectionRead)
def update_reflection(reflection_id: UUID, payload: ReflectionUpdate):
    service.update_reflection(reflection_id, payload.rating, payload.summary)
    return service.get_reflection_by_id(reflection_id)


@router.delete("/{reflection_id}", response_model=StatusMessage)
def delete_reflection(reflection_id: UUID):
    service.delete_reflection(reflection_id)
    return StatusMessage(message="Reflection deleted.")

