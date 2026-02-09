from uuid import UUID as UUID_TYPE

from pydantic import BaseModel

from app.schemas.activity import ActivityResponse
from app.schemas.building import BuildingResponse

class OrganisationResponse(BaseModel):
    id: UUID_TYPE
    name: str
    building_id: UUID_TYPE


class OrganisationDetailResponse(BaseModel):
    id: UUID_TYPE
    name: str
    building: BuildingResponse
    phone_numbers: list[str | None]
    activities: list[ActivityResponse]
