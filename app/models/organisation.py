from datetime import datetime, UTC
from uuid import UUID as UUID_TYPE, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
if TYPE_CHECKING:
    from app.models.building import Building
    from app.models.activity import Activity


class Organisation(Base):
    __tablename__ = "organisations"

    id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    building_id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("buildings.id", ondelete="RESTRICT")
    )   # Запрет удаления здания, если в нем организация
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Relationships
    building: Mapped["Building"] = relationship(back_populates="organisations")
    phones: Mapped[list["OrganisationPhone"]] = relationship(
        back_populates="organisation",
        cascade='all, delete-orphan'
    )   # При удалении организации: каскадное удаление номеров телефона
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organisation_activities",
        back_populates="organisations"
    )



class OrganisationPhone(Base):
    __tablename__ = "organisation_phones"

    id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    organisation_id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE")
    )
    phone_number: Mapped[str] = mapped_column(String(20))

    # Relationships
    organisation: Mapped["Organisation"] = relationship(back_populates="phones")