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