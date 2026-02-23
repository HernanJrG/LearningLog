from typing import Optional

from psycopg2 import IntegrityError, errorcodes

from app.business.errors import ConflictError, NotFoundError, ValidationError
from app.daos.resources import ResourceDAO


class ResourceService:
    def __init__(self, dao: Optional[ResourceDAO] = None):
        self.dao = dao or ResourceDAO()

    def create_resource(self, topic_id, title: str, url: str, resource_type: str):
        title = title.strip()
        url = url.strip()
        resource_type = resource_type.strip()
        if not title:
            raise ValidationError("Resource title is required.")
        if not url:
            raise ValidationError("Resource URL is required.")
        if not resource_type:
            raise ValidationError("Resource type is required.")

        try:
            return self.dao.create(topic_id, title, url, resource_type)
        except IntegrityError as exc:
            code = getattr(exc, "pgcode", None)
            if code == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("This topic already has a resource with that title.") from exc
            if code == errorcodes.FOREIGN_KEY_VIOLATION:
                raise NotFoundError("Topic not found.") from exc
            raise

    def get_resource_by_id(self, resource_id):
        resource = self.dao.get_by_id(resource_id)
        if not resource:
            raise NotFoundError("Resource not found.")
        return resource

    def list_resources_by_topic(self, topic_id):
        return self.dao.list_by_topic(topic_id)

    def update_resource(self, resource_id, title: str, url: str, resource_type: str) -> bool:
        title = title.strip()
        url = url.strip()
        resource_type = resource_type.strip()
        if not title:
            raise ValidationError("Resource title is required.")
        if not url:
            raise ValidationError("Resource URL is required.")
        if not resource_type:
            raise ValidationError("Resource type is required.")

        try:
            updated = self.dao.update(resource_id, title, url, resource_type)
        except IntegrityError as exc:
            if getattr(exc, "pgcode", None) == errorcodes.UNIQUE_VIOLATION:
                raise ConflictError("This topic already has a resource with that title.") from exc
            raise

        if not updated:
            raise NotFoundError("Resource not found.")
        return True

    def delete_resource(self, resource_id) -> bool:
        deleted = self.dao.delete(resource_id)
        if not deleted:
            raise NotFoundError("Resource not found.")
        return True

