from pydantic import BaseModel, Field


class GeoSearchParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    radius_km: float = Field(..., gt=0, description="Radius, km")
