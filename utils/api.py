from typing import Any, Optional, Dict, Union
from django.http import JsonResponse
from .constants import SUCCESS


def api_response(
    data: Any = None,
    message: str = SUCCESS,
    status_code: int = 200,
    error: Optional[Union[str, Dict[str, list[str]]]] = None,
) -> JsonResponse:
    """
    Create a standardized API response with consistent format.

    Args:
        data: The data to be included in the response. Can be any serializable type.
        message: A string message describing the response status.
        status_code: HTTP status code for the response.
        error: Error message or dictionary of field errors if any.

    Returns:
        JsonResponse: A Django JsonResponse object with the following format:
        {
            "message": str,
            "status_code": int,
            "error": Optional[Union[str, Dict[str, list[str]]]],
            "data": Any
        }

    Example:
        >>> api_response(data={"user": "john"}, message="Success", status_code=200)
        >>> api_response(message="Error", error="Invalid input", status_code=400)
    """
    response_data: Dict[str, Any] = {
        "message": message,
        "status_code": status_code,
        "error": error,
        "data": data,
    }

    return JsonResponse(response_data, status=status_code)
