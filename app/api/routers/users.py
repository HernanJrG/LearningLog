from typing import List
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.schemas import StatusMessage, UserCreate, UserRead, UserUpdate
from app.business.users_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    user_id = service.create_user(payload.full_name, payload.email)
    return service.get_user_by_id(user_id)


@router.get("", response_model=List[UserRead])
def list_users():
    return service.list_users()


@router.get("/by-email", response_model=UserRead)
def get_user_by_email(email: str = Query(..., min_length=1)):
    return service.get_user_by_email(email)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID):
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, payload: UserUpdate):
    service.update_user(user_id, payload.full_name, payload.email)
    return service.get_user_by_id(user_id)


@router.delete("/{user_id}", response_model=StatusMessage)
def delete_user(user_id: UUID):
    service.delete_user(user_id)
    return StatusMessage(message="User deleted.")

