# HTTP Status Code Constants
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
CONFLICT = 409
INTERNAL_SERVER_ERROR = 500

# Error Code Constants
VALIDATION_ERROR = "VALIDATION_ERROR"
NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
UNAUTHORIZED_ERROR = "UNAUTHORIZED_ERROR"
FORBIDDEN_ERROR = "FORBIDDEN_ERROR"
CONFLICT_ERROR = "CONFLICT_ERROR"
SERVER_ERROR = "SERVER_ERROR"

# Error Type Categories
VALIDATION = "validation"
AUTHENTICATION = "authentication"
AUTHORIZATION = "authorization"
SERVER = "server"

# Map error codes to HTTP status codes and error types
ERROR_CODE_MAP = {
    VALIDATION_ERROR: {
        "status_code": BAD_REQUEST,
        "error_type": VALIDATION
    },
    NOT_FOUND_ERROR: {
        "status_code": NOT_FOUND,
        "error_type": SERVER
    },
    UNAUTHORIZED_ERROR: {
        "status_code": UNAUTHORIZED,
        "error_type": AUTHENTICATION
    },
    FORBIDDEN_ERROR: {
        "status_code": FORBIDDEN,
        "error_type": AUTHORIZATION
    },
    CONFLICT_ERROR: {
        "status_code": CONFLICT,
        "error_type": VALIDATION
    },
    SERVER_ERROR: {
        "status_code": INTERNAL_SERVER_ERROR,
        "error_type": SERVER
    }
}


""" Use to handle http status code exceptions """
HTTP_ERROR_MAP = {
    BAD_REQUEST: {
        "error_code": VALIDATION_ERROR,
        "error_message": "Bad request"
    },
    UNAUTHORIZED: {
        "error_code": UNAUTHORIZED_ERROR,
        "error_message": "Authentication required"
    },
    FORBIDDEN: {
        "error_code": FORBIDDEN_ERROR,
        "error_message": "Access forbidden"
    },
    NOT_FOUND: {
        "error_code": NOT_FOUND_ERROR,
        "error_message": "Resource not found"
    },
    CONFLICT: {
        "error_code": CONFLICT_ERROR,
        "error_message": "Resource conflict"
    },
    INTERNAL_SERVER_ERROR: {
        "error_code": SERVER_ERROR,
        "error_message": "Internal server error"
    }
}

""" use for rasising proper exceptions """
class SilverAppException(Exception):
    """
    Base exception class for Silver App.
    
    All custom exceptions should inherit from this class to ensure
    consistent error handling and formatting.
    """
    
    def __init__(self, error_code, error_message, debug_message=None):
        """
        Initialize a Silver App exception.
        
        Args:
            error_code: Error code constant (e.g., VALIDATION_ERROR)
            error_message: User-friendly error message
            debug_message: Technical details for debugging (optional)
        """
        super().__init__(error_message)
        
        # Validate error code exists in our mapping
        if error_code not in ERROR_CODE_MAP:
            raise ValueError(f"Unknown error code: {error_code}")
        
        self.error_code = error_code
        self.error_message = error_message
        self.debug_message = debug_message
        
        # Get status code and error type from mapping
        error_info = ERROR_CODE_MAP[error_code]
        self.status_code = error_info["status_code"]
        self.error_type = error_info["error_type"]
    
    def to_dict(self):
        """
        Convert exception to dictionary format for JSON responses.
        
        Returns:
            dict: Exception data in standardized format
        """
        error_detail = {
            "error_code": self.error_code,
            "error_type": self.error_type,
            "error_message": self.error_message
        }
        
        # Add debug message if provided
        if self.debug_message:
            error_detail["debug_message"] = self.debug_message
            
        return error_detail

# Convenience exception classes for common scenarios
class ValidationException(SilverAppException):
    """Exception for validation errors."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(VALIDATION_ERROR, error_message, debug_message)


class NotFoundException(SilverAppException):
    """Exception for not found errors."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(NOT_FOUND_ERROR, error_message, debug_message)


class UnauthorizedException(SilverAppException):
    """Exception for unauthorized access errors."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(UNAUTHORIZED_ERROR, error_message, debug_message)


class ForbiddenException(SilverAppException):
    """Exception for forbidden access errors."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(FORBIDDEN_ERROR, error_message, debug_message)


class ConflictException(SilverAppException):
    """Exception for conflict errors (e.g., duplicate resources)."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(CONFLICT_ERROR, error_message, debug_message)


class ServerException(SilverAppException):
    """Exception for internal server errors."""
    
    def __init__(self, error_message, debug_message=None):
        super().__init__(SERVER_ERROR, error_message, debug_message)