from typing import Optional

from app.db import get_cursor


class TopicDAO:
    def create(self, user_id, name: str, description: Optional[str]):
        sql = """
            INSERT INTO topics (user_id, name, description)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        with get_cursor() as cur:
            cur.execute(sql, (user_id, name, description))
            return cur.fetchone()["id"]

    def get_by_id(self, topic_id):
        sql = """
            SELECT id, user_id, name, description, created_at
            FROM topics
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (topic_id,))
            return cur.fetchone()

    def list_all(self):
        sql = """
            SELECT id, user_id, name, description, created_at
            FROM topics
            ORDER BY created_at DESC
        """
        with get_cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def list_by_user(self, user_id):
        sql = """
            SELECT id, user_id, name, description, created_at
            FROM topics
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchall()

    def update(self, topic_id, name: str, description: Optional[str]) -> bool:
        sql = """
            UPDATE topics
            SET name = %s, description = %s
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (name, description, topic_id))
            return cur.rowcount > 0

    def delete(self, topic_id) -> bool:
        sql = "DELETE FROM topics WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (topic_id,))
            return cur.rowcount > 0
