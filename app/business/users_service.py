from typing import Optional

from psycopg2 import IntegrityError, errorcodes

from app.business.errors import ConflictError, NotFoundError, ValidationError
from app.daos.users import UserDAO


class UserService:
    def __init__(self, dao: Optional[UserDAO] = None):
        self.dao = dao or UserDAO()

    def create_user(self, full_name: str, email: str):
        full_name = full_name.strip()
        email = email.strip()
        if not full_name:
            raise ValidationError("Full name is required.")
        if not email:
            raise ValidationError("Email is required.")

        try:
            return self.dao.create(full_name, email)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("A user with this email already exists.") from exc
            raise

    def get_user_by_id(self, user_id):
        user = self.dao.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user

    def get_user_by_email(self, email: str):
        email = email.strip()
        if not email:
            raise ValidationError("Email is required.")
        user = self.dao.get_by_email(email)
        if not user:
            raise NotFoundError("User not found.")
        return user

    def list_users(self):
        return self.dao.list_all()

    def update_user(self, user_id, full_name: str, email: str) -> bool:
        full_name = full_name.strip()
        email = email.strip()
        if not full_name:
            raise ValidationError("Full name is required.")
        if not email:
            raise ValidationError("Email is required.")

        try:
            updated = self.dao.update(user_id, full_name, email)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("A user with this email already exists.") from exc
            raise

        if not updated:
            raise NotFoundError("User not found.")
        return True

    def delete_user(self, user_id) -> bool:
        deleted = self.dao.delete(user_id)
        if not deleted:
            raise NotFoundError("User not found.")
        return True
