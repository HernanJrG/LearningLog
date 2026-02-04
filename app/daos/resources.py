from app.db import get_cursor


class ResourceDAO:
    def create(self, topic_id, title: str, url: str, resource_type: str):
        sql = """
            INSERT INTO resources (topic_id, title, url, resource_type)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        with get_cursor() as cur:
            cur.execute(sql, (topic_id, title, url, resource_type))
            return cur.fetchone()["id"]

    def get_by_id(self, resource_id):
        sql = """
            SELECT id, topic_id, title, url, resource_type, created_at
            FROM resources
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (resource_id,))
            return cur.fetchone()

    def list_by_topic(self, topic_id):
        sql = """
            SELECT id, topic_id, title, url, resource_type, created_at
            FROM resources
            WHERE topic_id = %s
            ORDER BY created_at DESC
        """
        with get_cursor() as cur:
            cur.execute(sql, (topic_id,))
            return cur.fetchall()

    def update(self, resource_id, title: str, url: str, resource_type: str) -> bool:
        sql = """
            UPDATE resources
            SET title = %s, url = %s, resource_type = %s
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (title, url, resource_type, resource_id))
            return cur.rowcount > 0

    def delete(self, resource_id) -> bool:
        sql = "DELETE FROM resources WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (resource_id,))
            return cur.rowcount > 0
