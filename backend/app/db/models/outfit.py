from sqlalchemy import TEXT, TIMESTAMP, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Outfit(Base):
    __tablename__ = "outfits"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    preview_image_url: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True)
