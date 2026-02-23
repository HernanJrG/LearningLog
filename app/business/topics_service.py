from typing import Optional

from psycopg2 import IntegrityError, errorcodes

from app.business.errors import ConflictError, NotFoundError, ValidationError
from app.daos.topics import TopicDAO


class TopicService:
    def __init__(self, dao: Optional[TopicDAO] = None):
        self.dao = dao or TopicDAO()

    def create_topic(self, user_id, name: str, description: Optional[str]):
        name = name.strip()
        description = description.strip() if isinstance(description, str) else None
        if not name:
            raise ValidationError("Topic name is required.")

        try:
            return self.dao.create(user_id, name, description)
        except IntegrityError as exc:
            code = getattr(exc, "pgcode", None)
            if code == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("This user already has a topic with that name.") from exc
            if code == errorcodes.FOREIGN_KEY_VIOLATION:
                raise NotFoundError("User not found.") from exc
            raise

    def get_topic_by_id(self, topic_id):
        topic = self.dao.get_by_id(topic_id)
        if not topic:
            raise NotFoundError("Topic not found.")
        return topic

    def list_topics(self):
        return self.dao.list_all()

    def list_topics_by_user(self, user_id):
        return self.dao.list_by_user(user_id)

    def update_topic(self, topic_id, name: str, description: Optional[str]) -> bool:
        name = name.strip()
        description = description.strip() if isinstance(description, str) else None
        if not name:
            raise ValidationError("Topic name is required.")

        try:
            updated = self.dao.update(topic_id, name, description)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("This user already has a topic with that name.") from exc
            raise

        if not updated:
            raise NotFoundError("Topic not found.")
        return True

    def delete_topic(self, topic_id) -> bool:
        deleted = self.dao.delete(topic_id)
        if not deleted:
            raise NotFoundError("Topic not found.")
        return True

