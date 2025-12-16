class InvalidCredentialsError(Exception):
    """Raised when upstream says credentials are invalid."""
    pass


class UnauthorizedTokenError(Exception):
    """Raised when token is invalid/expired."""
    pass


class UpstreamServiceError(Exception):
    """Raised when upstream fails unexpectedly."""
    pass