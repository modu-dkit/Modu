from sqlalchemy import JSON, DECIMAL, ForeignKey, String, TEXT, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OwnedClothes(Base):
    __tablename__ = "owned_clothes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    color: Mapped[str | None] = mapped_column(String(80), nullable=True)
    tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    embedding: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    size_label: Mapped[str | None] = mapped_column(String(30), nullable=True)
    image_s3_url: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
