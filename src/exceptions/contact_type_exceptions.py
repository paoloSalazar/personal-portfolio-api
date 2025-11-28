class ContactTypeException(Exception):
    """Base exception for contactType-related errors"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ContactTypeAlreadyExistsException(ContactTypeException):
    """Raised when trying to create a contact type that already exists"""
    def __init__(self, name):
        message = f"ContactType with name {name} already exists"
        super().__init__(message, 409)

class ContactTypeDatabaseException(ContactTypeException):
    """Raised for general database errors"""
    def __init__(self, message="Database error occurred"):
        super().__init__(message, 500)