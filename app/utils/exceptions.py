from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class HealthcareException(HTTPException):
    """Base exception class for healthcare API"""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class DatabaseException(HealthcareException):
    """Exception for database errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class NotFoundException(HealthcareException):
    """Exception for resource not found"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found"
        )

class AuthenticationException(HealthcareException):
    """Exception for authentication errors"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(HealthcareException):
    """Exception for authorization errors"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ValidationException(HealthcareException):
    """Exception for validation errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class FileUploadException(HealthcareException):
    """Exception for file upload errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload error: {detail}"
        )