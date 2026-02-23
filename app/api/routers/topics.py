from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.schemas import StatusMessage, TopicCreate, TopicRead, TopicUpdate
from app.business.topics_service import TopicService

router = APIRouter(prefix="/topics", tags=["topics"])
service = TopicService()


@router.post("", response_model=TopicRead, status_code=status.HTTP_201_CREATED)
def create_topic(payload: TopicCreate):
    topic_id = service.create_topic(payload.user_id, payload.name, payload.description)
    return service.get_topic_by_id(topic_id)


@router.get("", response_model=List[TopicRead])
def list_topics(user_id: Optional[UUID] = Query(default=None)):
    if user_id is None:
        return service.list_topics()
    return service.list_topics_by_user(user_id)


@router.get("/{topic_id}", response_model=TopicRead)
def get_topic(topic_id: UUID):
    return service.get_topic_by_id(topic_id)


@router.put("/{topic_id}", response_model=TopicRead)
def update_topic(topic_id: UUID, payload: TopicUpdate):
    service.update_topic(topic_id, payload.name, payload.description)
    return service.get_topic_by_id(topic_id)


@router.delete("/{topic_id}", response_model=StatusMessage)
def delete_topic(topic_id: UUID):
    service.delete_topic(topic_id)
    return StatusMessage(message="Topic deleted.")

