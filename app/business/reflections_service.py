from typing import Optional

from psycopg2 import IntegrityError, errorcodes

from app.business.errors import NotFoundError, ValidationError
from app.daos.reflections import ReflectionDAO


class ReflectionService:
    def __init__(self, dao: Optional[ReflectionDAO] = None):
        self.dao = dao or ReflectionDAO()

    def create_reflection(self, session_id, rating: int, summary: str):
        summary = summary.strip()
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        if not summary:
            raise ValidationError("Summary is required.")

        try:
            return self.dao.create(session_id, rating, summary)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.FOREIGN_KEY_VIOLATION:
                raise NotFoundError("Learning session not found.") from exc
            raise

    def get_reflection_by_id(self, reflection_id):
        reflection = self.dao.get_by_id(reflection_id)
        if not reflection:
            raise NotFoundError("Reflection not found.")
        return reflection

    def list_reflections_by_session(self, session_id):
        return self.dao.list_by_session(session_id)

    def list_reflections_by_topic(self, topic_id):
        return self.dao.list_by_topic(topic_id)

    def update_reflection(self, reflection_id, rating: int, summary: str) -> bool:
        summary = summary.strip()
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        if not summary:
            raise ValidationError("Summary is required.")

        updated = self.dao.update(reflection_id, rating, summary)
        if not updated:
            raise NotFoundError("Reflection not found.")
        return True

    def delete_reflection(self, reflection_id) -> bool:
        deleted = self.dao.delete(reflection_id)
        if not deleted:
            raise NotFoundError("Reflection not found.")
        return True

