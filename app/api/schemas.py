from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StatusMessage(BaseModel):
    message: str


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)


class UserRead(BaseModel):
    id: UUID
    full_name: str
    email: str
    created_at: datetime


class TopicCreate(BaseModel):
    user_id: UUID
    name: str = Field(min_length=1)
    description: Optional[str] = None


class TopicUpdate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None


class TopicRead(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    created_at: datetime


class ResourceCreate(BaseModel):
    topic_id: UUID
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    resource_type: str = Field(min_length=1)


class ResourceUpdate(BaseModel):
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    resource_type: str = Field(min_length=1)


class ResourceRead(BaseModel):
    id: UUID
    topic_id: UUID
    title: str
    url: str
    resource_type: str
    created_at: datetime


class LearningSessionCreate(BaseModel):
    user_id: UUID
    topic_id: UUID
    session_date: date
    duration_minutes: int = Field(gt=0)
    notes: Optional[str] = None


class LearningSessionUpdate(BaseModel):
    session_date: date
    duration_minutes: int = Field(gt=0)
    notes: Optional[str] = None


class LearningSessionRead(BaseModel):
    id: UUID
    user_id: UUID
    topic_id: UUID
    session_date: date
    duration_minutes: int
    notes: Optional[str]
    created_at: datetime


class ReflectionCreate(BaseModel):
    session_id: UUID
    rating: int = Field(ge=1, le=5)
    summary: str = Field(min_length=1)


class ReflectionUpdate(BaseModel):
    rating: int = Field(ge=1, le=5)
    summary: str = Field(min_length=1)


class ReflectionRead(BaseModel):
    id: UUID
    session_id: UUID
    rating: int
    summary: str
    created_at: datetime

