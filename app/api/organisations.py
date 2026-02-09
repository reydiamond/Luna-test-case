import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID as UUID_TYPE

from app.database import get_session
from app.models import Organisation, OrganisationPhone, Activity, Building
from app.schemas import OrganisationResponse, OrganisationDetailResponse

router = APIRouter()

@router.get("/organisations/search", response_model=list[OrganisationResponse])
async def search_organisations_by_name(
        name: Annotated[str, Query(min_length=1, description="Название организации")],
        db: AsyncSession = Depends(get_session)
):
    """
    Поиск организаций по названию
    """

    result = await db.execute(
        select(Organisation)
        .where(Organisation.name.ilike(f"%{name}%"))
        .order_by(Organisation.name)
    )

    organisations = result.scalars().all()

    return organisations

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    R = 6371.0  # Радиус Земли в км

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Формула гаверсинусов
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


@router.get("/organisations/nearby", response_model=list[OrganisationResponse])
async def get_organisations_nearby(
        latitude: Annotated[float, Query(ge=-90, le=90, description="Широта центра поиска")],
        longitude: Annotated[float, Query(ge=-180, le=180, description="Долгота центра поиска")],
        radius_km: Annotated[float, Query(gt=0, le=100, description="Радиус поиска в км (макс 100)")],
        db: AsyncSession = Depends(get_session)
):
    """
    Геопоиск по радиусу
    """
    result = await db.execute(
        select(Organisation)
        .options(selectinload(Organisation.building))
    )
    all_organisations = result.scalars().all()

    nearby_organisations = []

    for org in all_organisations:
        if org.building:
            distance = calculate_distance(
                latitude, longitude,
                float(org.building.latitude), float(org.building.longitude)
            )

            if distance <= radius_km:
                nearby_organisations.append(org)

    return nearby_organisations


@router.get("/organisations/{organisation_id}", response_model=OrganisationDetailResponse)
async def get_organisation_by_id(
        organisation_id: Annotated[UUID_TYPE, Path(description="ID компании")],
        db: AsyncSession = Depends(get_session)
):
    """
    Вывод информации об организации по её идентификатору
    """

    result = await db.execute(
        select(Organisation).options(
            selectinload(Organisation.building),
            selectinload(Organisation.phones),
            selectinload(Organisation.activities),
        ).where(Organisation.id == organisation_id)
    )
    organisation = result.scalar_one_or_none()

    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")

    response_data = OrganisationDetailResponse.model_validate(organisation)
    response_data.phone_numbers = [phone.phone_number for phone in organisation.phones]

    return response_data



@router.get("/organisations", response_model=list[OrganisationResponse])
async def get_organisations_by_filters(
        building_id: Annotated[UUID_TYPE, Query(description="Фильтр по зданию")] = None,
        activity_id: Annotated[UUID_TYPE, Query(description="Фильтр по деятельности")] = None,
        db: AsyncSession = Depends(get_session)
):
    """
    Поиск организаций по фильтрам
    """

    query = select(Organisation)

    if building_id:
        query = query.where(Organisation.building_id == building_id)

    if activity_id:
        activity_ids = await get_activity_tree_ids(db, activity_id)

        query = query.join(Organisation.activities).where(Activity.id.in_(activity_ids))

    result = await db.execute(query.order_by(Organisation.name))
    organisations = result.scalars().all()

    return organisations


async def get_activity_tree_ids(db: AsyncSession, activity_id: UUID_TYPE) -> list[UUID_TYPE]:

    """
    Функция получения ID деятельности и всех потомков
    """

    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    if not activity:
        return []

    ids = [activity.id]

    result = await db.execute(
        select(Activity).where(Activity.parent_id == activity_id)
    )
    children = result.scalars().all()

    for child in children:
        child_ids = await get_activity_tree_ids(db, child.id)
        ids.extend(child_ids)

    return ids


