from sqlalchemy import DECIMAL, TIMESTAMP, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    height_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    bust_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    hip_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True)
