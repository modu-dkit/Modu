from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OutfitItem(Base):
    __tablename__ = "outfit_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    outfit_id: Mapped[str] = mapped_column(ForeignKey("outfits.id"), nullable=False)
    owned_clothes_id: Mapped[str | None] = mapped_column(
        ForeignKey("owned_clothes.id"), nullable=True
    )
    shop_product_id: Mapped[str | None] = mapped_column(
        ForeignKey("shop_products.id"), nullable=True
    )
