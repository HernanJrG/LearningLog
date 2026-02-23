from typing import List
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.schemas import ResourceCreate, ResourceRead, ResourceUpdate, StatusMessage
from app.business.resources_service import ResourceService

router = APIRouter(prefix="/resources", tags=["resources"])
service = ResourceService()


@router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
def create_resource(payload: ResourceCreate):
    resource_id = service.create_resource(
        payload.topic_id,
        payload.title,
        payload.url,
        payload.resource_type,
    )
    return service.get_resource_by_id(resource_id)


@router.get("", response_model=List[ResourceRead])
def list_resources_by_topic(topic_id: UUID = Query(...)):
    return service.list_resources_by_topic(topic_id)


@router.get("/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: UUID):
    return service.get_resource_by_id(resource_id)


@router.put("/{resource_id}", response_model=ResourceRead)
def update_resource(resource_id: UUID, payload: ResourceUpdate):
    service.update_resource(resource_id, payload.title, payload.url, payload.resource_type)
    return service.get_resource_by_id(resource_id)


@router.delete("/{resource_id}", response_model=StatusMessage)
def delete_resource(resource_id: UUID):
    service.delete_resource(resource_id)
    return StatusMessage(message="Resource deleted.")

