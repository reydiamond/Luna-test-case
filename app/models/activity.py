from datetime import datetime, UTC
from uuid import UUID as UUID_TYPE, uuid4
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
if TYPE_CHECKING:
    from app.models.organisation import Organisation


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    parent_id: Mapped[Optional[UUID_TYPE]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="RESTRICT"),
        nullable=True
    )
    level: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Constraints
    # Ограничения:
    # по вложенности деятельностей;
    # по наличию родительской деятельности.
    __table_args__ = (
        CheckConstraint(
            "level >= 1 AND level <= 3",
            name="check_level_range"),
        CheckConstraint(
            "(parent_id IS NULL AND level = 1) OR (parent_id IS NOT NULL AND level > 1)",
            name="check_parent_level")
    )

    # Relationships
    parent: Mapped[Optional["Activity"]] = relationship(
        back_populates="children",
        remote_side=[id]
    )   # One to one
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
    organisations: Mapped[list["Organisation"]] = relationship(
        secondary="organisation_activities",
        back_populates="activities"
    )   # Many to many