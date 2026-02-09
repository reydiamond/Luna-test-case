from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from app.core.config import get_settings

settings = get_settings()

api_key_header = APIKeyHeader(name="Static_API_key", auto_error=True)

async def verify_api_key(static_api_key: str = Security(api_key_header)):
    if static_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return static_api_key