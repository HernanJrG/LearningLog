"""Business-layer exception types."""


class BusinessError(Exception):
    """Base class for all business-layer errors."""


class ValidationError(BusinessError):
    """Raised when input fails business-layer validation."""


class NotFoundError(BusinessError):
    """Raised when a requested record does not exist."""


class ConflictError(BusinessError):
    """Raised when a record violates a uniqueness or conflict rule."""

