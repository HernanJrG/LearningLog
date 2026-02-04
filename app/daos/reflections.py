from app.db import get_cursor


class ReflectionDAO:
    def create(self, session_id, rating: int, summary: str):
        sql = """
            INSERT INTO reflections (session_id, rating, summary)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        with get_cursor() as cur:
            cur.execute(sql, (session_id, rating, summary))
            return cur.fetchone()["id"]

    def get_by_id(self, reflection_id):
        sql = """
            SELECT id, session_id, rating, summary, created_at
            FROM reflections
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (reflection_id,))
            return cur.fetchone()

    def list_by_session(self, session_id):
        sql = """
            SELECT id, session_id, rating, summary, created_at
            FROM reflections
            WHERE session_id = %s
            ORDER BY created_at DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (session_id,))
            return cur.fetchall()

    def list_by_topic(self, topic_id):
        sql = """
            SELECT r.id, r.session_id, r.rating, r.summary, r.created_at
            FROM reflections r
            JOIN learning_sessions ls ON r.session_id = ls.id
            WHERE ls.topic_id = %s
            ORDER BY r.created_at DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (topic_id,))
            return cur.fetchall()

    def update(self, reflection_id, rating: int, summary: str) -> bool:
        sql = """
            UPDATE reflections
            SET rating = %s, summary = %s
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (rating, summary, reflection_id))
            return cur.rowcount > 0

    def delete(self, reflection_id) -> bool:
        sql = "DELETE FROM reflections WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (reflection_id,))
            return cur.rowcount > 0
