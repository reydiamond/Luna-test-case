from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

'''
Таблица Many to many для связей организаций и типов деятельности
'''

organisation_activities = Table(
    "organisation_activities",
    Base.metadata,
    Column(
        "organisation_id",
        UUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "activity_id",
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="RESTRICT"),
        primary_key=True
    )
)