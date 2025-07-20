""" Contains standardizd responese """

from flask import g, request, jsonify
import datetime as dt
import functools


def success_response(data, message="", status_code= 200, metadata = None):
    """
    Generate a standardized success response.
    
    Args:
        data: The response data (any JSON-serializable object)
        message: Success message (default: empty string)
        status_code: HTTP status code (default: 200)
        metadata: Additional metadata dict (default: empty dict)
    
    Returns:
        tuple: (jsonified_response, status_code)
    
    Response format:
        {
            "success": true,
            "api_version": "v1",
            "blueprint": "blueprint_name",
            "timestamp": "2025-07-20T10:30:45Z",
            "request_id": "req_20250720_103045_abc123",
            "message": "Operation completed successfully",
            "data": { ... },
            "metadata": { ... },
            "status_code": 200
        }
    """
    metadata = metadata or {}

    request_id =  getattr(g, "request_id", "unknown")

    blueprint_name = request.blueprint if request.blueprint else "app"
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')
    response_dict = {
        "success": True,
        "api_version": "v1",
        "blueprint": blueprint_name,
        "timestamp": timestamp,
        "request_id": request_id,
        "message": message,
        "data": data,
        "metadata": metadata,
        "status_code": status_code
    }
    
    return jsonify(response_dict), status_code



def success_response_decorator(message="", status_code=200):


    """
    Decorator that automatically wraps view function returns in standardized response format.
    
    View functions must return a tuple:
    - Length 1: (data,) - Just data, metadata will be {}
    - Length 2: (data, metadata) - Data with custom metadata
    
    Args:
        message: Success message for the response
        status_code: HTTP status code (default: 200)
    
    Usage:
        @success_response_decorator("Users retrieved successfully")
        def get_users():
            return (users_data,)  # Just data
            
        @success_response_decorator("Users retrieved successfully") 
        def get_paginated_users():
            page = int(request.args.get('page', 1))
            users = fetch_users(page)
            metadata = {"page": page, "total": 100}
            return (users, metadata)  # Data + metadata
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Ensure result is a tuple
            if not isinstance(result, tuple):
                raise ValueError(f"View function '{func.__name__}' must return a tuple of length 1 or 2")
            
            # Handle different tuple lengths
            if len(result) == 1:
                data = result[0]
                metadata = {}
            elif len(result) == 2:
                data, metadata = result
            else:
                raise ValueError(f"View function '{func.__name__}' must return a tuple of length 1 or 2, got length {len(result)}")
            
            return success_response(data, message, status_code, metadata)
        
        return wrapper
    return decorator



def error_response(exception):

    """
    Generate a standardized error response from a SilverAppException.
    
    Args:
        exception: SilverAppException object containing error details
    
    Returns:
        tuple: (jsonified_response, status_code)
    
    Response format:
        {
            "success": false,
            "error_id": "req_20250720_103045_abc123",
            "api_version": "v1", 
            "blueprint": "blueprint_name",
            "timestamp": "2025-07-20T10:30:45Z",
            "error_detail": {
                "error_code": "VALIDATION_ERROR",
                "error_type": "validation",
                "error_message": "Username is required",
                "debug_message": "Field 'username' cannot be empty"
            },
            "status_code": 400
        }
    """
    # Get request ID from Flask g (same as success responses)
    request_id = getattr(g, 'request_id', 'unknown')
    
    # Get blueprint name, fallback to "app"
    blueprint_name = request.blueprint if request.blueprint else "app"
    
    # Generate response timestamp in ISO format
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Get error details from exception object
    error_detail = exception.to_dict()
    
    # Build standardized error response structure
    response_dict = {
        "success": False,
        "error_id": request_id,  # Same as request_id for tracing
        "api_version": "v1",
        "blueprint": blueprint_name,
        "timestamp": timestamp,
        "error_detail": error_detail,
        "status_code": exception.status_code
    }
    
    return jsonify(response_dict), exception.status_code




def handle_silver_app_exception(exception):
    """
    Global error handler for all SilverAppException instances.
    
    This function is registered with Flask's error handling system
    to automatically catch and format any SilverAppException raised
    anywhere in the application.
    
    Args:
        exception: SilverAppException object
    
    Returns:
        Standardized error response
    """
    return error_response(exception)


def handle_http_exception(error):
    """
    Handle HTTP exceptions and convert to standardized format.
    
    Maps common HTTP status codes to appropriate SilverAppException types
    using the centralized HTTP_ERROR_MAP from errors.py.
    Falls back to ServerException for unmapped status codes.
    
    Args:
        error: Flask's HTTPException object
    
    Returns:
        Standardized error response
    """
    from silver_app.utils.errors import (
        SilverAppException, HTTP_ERROR_MAP, SERVER_ERROR
    )
    
    # Get mapping for this HTTP status code
    if error.code in HTTP_ERROR_MAP:
        error_mapping = HTTP_ERROR_MAP[error.code]
        error_code = error_mapping["error_code"]
        error_message = error_mapping["error_message"]
        debug_message = f"HTTP {error.code}: {error.description}"
    else:
        # Fallback for any unmapped HTTP status codes
        error_code = SERVER_ERROR
        error_message = f"HTTP {error.code} error occurred"
        debug_message = f"HTTP {error.code}: {error.description}"
    
    # Create the appropriate exception
    exception = SilverAppException(error_code, error_message, debug_message)
    
    return error_response(exception)


def handle_generic_exception(error):
    """
    Handle any unhandled exceptions and convert to standardized format.
    
    This is a catch-all for any exceptions that don't have specific handlers.
    
    Args:
        error: Any Python exception
    
    Returns:
        Standardized error response
    """
    from silver_app.utils.errors import ServerException
    
    exception = ServerException(
        "An unexpected error occurred",
        f"Unhandled exception: {type(error).__name__}: {str(error)}"
    )
    return error_response(exception)