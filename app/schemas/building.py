from uuid import UUID as UUID_TYPE

from pydantic import BaseModel


class BuildingResponse(BaseModel):
    id: UUID_TYPE
    address: str
    latitude: float
    longitude: float
