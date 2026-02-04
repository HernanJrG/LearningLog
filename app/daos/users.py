from app.db import get_cursor


class UserDAO:
    def create(self, full_name: str, email: str):
        sql = """
            INSERT INTO users (full_name, email)
            VALUES (%s, %s)
            RETURNING id
        """
        with get_cursor() as cur:
            cur.execute(sql, (full_name, email))
            return cur.fetchone()["id"]

    def get_by_id(self, user_id):
        sql = "SELECT id, full_name, email, created_at FROM users WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchone()

    def get_by_email(self, email: str):
        sql = "SELECT id, full_name, email, created_at FROM users WHERE email = %s"
        with get_cursor() as cur:
            cur.execute(sql, (email,))
            return cur.fetchone()

    def list_all(self):
        sql = "SELECT id, full_name, email, created_at FROM users ORDER BY full_name"
        with get_cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def update(self, user_id, full_name: str, email: str) -> bool:
        sql = """
            UPDATE users
            SET full_name = %s, email = %s
            WHERE id = %s
        """
        with get_cursor() as cur:
            cur.execute(sql, (full_name, email, user_id))
            return cur.rowcount > 0

    def delete(self, user_id) -> bool:
        sql = "DELETE FROM users WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.rowcount > 0
