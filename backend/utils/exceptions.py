class ServiceError(Exception):
    """Base class for all service-layer errors."""

    status_code = 400


class InvalidCredentialsError(ServiceError):
    """Credentials were provided but are wrong."""

    message = "Invalid username or password"
    status_code = 401

    def __str__(self):
        return self.message


class InvalidFileError(ServiceError):
    """File was received but can't be parsed/used."""

    message = "Uploaded file is not valid JSON."
    status_code = 422

    def __str__(self):
        return self.message


class MissingFileFieldError(ServiceError):
    """Valid JSON but doesn't match expected schema."""

    status_code = 422


class FieldWrongTypeError(ServiceError):
    """Field present but of the wrong type."""

    status_code = 422


class MissingFieldError(ServiceError):
    """A required field is absent from the payload."""

    status_code = 422


class InvalidEmailError(ServiceError):
    """Value is present but fails validation rules."""

    message = "Email format is invalid"
    status_code = 422

    def __str__(self):
        return self.message


class RepositoryError(Exception):
    """Base class for all repository-layer errors."""

    status_code = 400


class UserAlreadyExistsError(RepositoryError):
    """Request is valid but violates a uniqueness constraint."""

    message = "Username or email already in use"
    status_code = 409

    def __str__(self):
        return self.message


class JWTError(ServiceError):
    """Any token problem means the client must re-authenticate."""

    status_code = 401


class TokenExpiredError(JWTError):
    """Expired token."""

    message = "Token has expired"
    status_code = 401

    def __str__(self):
        return self.message


class InvalidTokenError(JWTError):
    """Malformed/tampered token."""

    message = "Token is invalid"
    status_code = 401

    def __str__(self):
        return self.message
