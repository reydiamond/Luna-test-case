from uuid import UUID as UUID_TYPE

from pydantic import BaseModel

class ActivityResponse(BaseModel):
    id: UUID_TYPE
    name: str
    level: int
    parent_id: UUID_TYPE | None = None



class ActivityTree(ActivityResponse):
    children: list["ActivityTree"] = []
