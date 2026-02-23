from typing import Optional

from psycopg2 import IntegrityError, errorcodes

from app.business.errors import NotFoundError, ValidationError
from app.daos.learning_sessions import LearningSessionDAO


class LearningSessionService:
    def __init__(self, dao: Optional[LearningSessionDAO] = None):
        self.dao = dao or LearningSessionDAO()

    def create_session(self, user_id, topic_id, session_date, duration_minutes: int, notes: Optional[str]):
        if duration_minutes <= 0:
            raise ValidationError("Duration must be greater than zero.")
        notes = notes.strip() if isinstance(notes, str) else None

        try:
            return self.dao.create(user_id, topic_id, session_date, duration_minutes, notes)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.FOREIGN_KEY_VIOLATION:
                raise NotFoundError("User or topic not found.") from exc
            raise

    def get_session_by_id(self, session_id):
        session = self.dao.get_by_id(session_id)
        if not session:
            raise NotFoundError("Learning session not found.")
        return session

    def list_sessions_by_user(self, user_id):
        return self.dao.list_by_user(user_id)

    def list_sessions_by_topic(self, topic_id):
        return self.dao.list_by_topic(topic_id)

    def update_session(self, session_id, session_date, duration_minutes: int, notes: Optional[str]) -> bool:
        if duration_minutes <= 0:
            raise ValidationError("Duration must be greater than zero.")
        notes = notes.strip() if isinstance(notes, str) else None

        updated = self.dao.update(session_id, session_date, duration_minutes, notes)
        if not updated:
            raise NotFoundError("Learning session not found.")
        return True

    def delete_session(self, session_id) -> bool:
        deleted = self.dao.delete(session_id)
        if not deleted:
            raise NotFoundError("Learning session not found.")
        return True

