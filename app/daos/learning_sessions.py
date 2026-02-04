from typing import Optional

from app.db import get_cursor


class LearningSessionDAO:
    def create(self, user_id, topic_id, session_date, duration_minutes: int, notes: Optional[str]):
        sql = """
            INSERT INTO learning_sessions (user_id, topic_id, session_date, duration_minutes, notes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        with get_cursor() as cur:
            cur.execute(sql, (user_id, topic_id, session_date, duration_minutes, notes))
            return cur.fetchone()["id"]

    def get_by_id(self, session_id):
        sql = """
            SELECT id, user_id, topic_id, session_date, duration_minutes, notes, created_at
            FROM learning_sessions
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (session_id,))
            return cur.fetchone()

    def list_by_user(self, user_id):
        sql = """
            SELECT id, user_id, topic_id, session_date, duration_minutes, notes, created_at
            FROM learning_sessions
            WHERE user_id = %s
            ORDER BY session_date DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchall()

    def list_by_topic(self, topic_id):
        sql = """
            SELECT id, user_id, topic_id, session_date, duration_minutes, notes, created_at
            FROM learning_sessions
            WHERE topic_id = %s
            ORDER BY session_date DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (topic_id,))
            return cur.fetchall()

    def update(self, session_id, session_date, duration_minutes: int, notes: Optional[str]) -> bool:
        sql = """
            UPDATE learning_sessions
            SET session_date = %s, duration_minutes = %s, notes = %s
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (session_date, duration_minutes, notes, session_id))
            return cur.rowcount > 0

    def delete(self, session_id) -> bool:
        sql = "DELETE FROM learning_sessions WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (session_id,))
            return cur.rowcount > 0
