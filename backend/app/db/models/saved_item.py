from sqlalchemy import TIMESTAMP, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SavedItem(Base):
    __tablename__ = "saved_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    shop_product_id: Mapped[str] = mapped_column(
        ForeignKey("shop_products.id"), nullable=False
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
