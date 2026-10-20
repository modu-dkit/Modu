from sqlalchemy import ForeignKey, String, TEXT, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TryOnJob(Base):
    __tablename__ = "try_on_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    outfit_id: Mapped[str | None] = mapped_column(ForeignKey("outfits.id"), nullable=True)
    result_s3_url: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
