class UserException(Exception):
    """Base exception for user-related errors"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UserNotFoundException(UserException):
    """Raised when a user is not found"""
    def __init__(self, user_id=None, email=None):
        if user_id:
            message = f"User with ID {user_id} not found"
        elif email:
            message = f"User with email {email} not found"
        else:
            message = "User not found"
        super().__init__(message, 404)

class UserAlreadyExistsException(UserException):
    """Raised when trying to create a user that already exists"""
    def __init__(self, email):
        message = f"User with email {email} already exists"
        super().__init__(message, 409)

class UserValidationException(UserException):
    """Raised when user data validation fails"""
    def __init__(self, message):
        super().__init__(message, 400)

class UserDatabaseException(UserException):
    """Raised for general database errors"""
    def __init__(self, message="Database error occurred"):
        super().__init__(message, 500)