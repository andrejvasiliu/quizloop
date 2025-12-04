class ServiceError(Exception):
    """Base class for all service-layer errors."""

    pass


class InvalidCredentialsError(ServiceError):
    message = "Invalid username or password"

    def __str__(self):
        return self.message


class InvalidFileError(ServiceError):
    message = "Uploaded file is not valid JSON."

    def __str__(self):
        return self.message


class MissingFileFieldError(ServiceError):
    """Payload is valid JSON but does not match schema."""

    pass


class FieldWrongTypeError(ServiceError):
    """Payload field is of the wrong type."""

    pass

class MissingFieldError(ServiceError):
    """Payload is missing a required field."""

    pass

class InvalidEmailError(ServiceError):
    message = "Email format is invalid"

    def __str__(self):
        return self.message


class RepositoryError(Exception):
    """Base class for all repository-layer errors."""

    pass


class UserAlreadyExistsError(RepositoryError):
    message = "Username or email already in use"

    def __str__(self):
        return self.message


class JWTError(ServiceError):
    pass


class TokenExpiredError(JWTError):
    message = "Token has expired"

    def __str__(self):
        return self.message


class InvalidTokenError(JWTError):
    message = "Token is invalid"

    def __str__(self):
        return self.message
