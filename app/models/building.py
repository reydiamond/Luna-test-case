from datetime import datetime, UTC
from uuid import UUID as UUID_TYPE, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
if TYPE_CHECKING:
    from app.models.organisation import Organisation


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    address: Mapped[str] = mapped_column(String(500))
    latitude: Mapped[float] = mapped_column(Numeric(10, 8))
    longitude: Mapped[float] = mapped_column(Numeric(11, 8))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Relationships
    organisations: Mapped[list["Organisation"]] = relationship(back_populates="building")