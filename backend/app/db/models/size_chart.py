from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SizeChart(Base):
    __tablename__ = "size_charts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    shop_product_id: Mapped[str] = mapped_column(
        ForeignKey("shop_products.id"), nullable=False
    )
    size_label: Mapped[str] = mapped_column(String(30), nullable=False)
    chest_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    hip_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    inseam_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    length_cm: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True)
