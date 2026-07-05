from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DECIMAL, DateTime, Boolean, func, ForeignKey

class Product(db.Model):
    
    __tablename__ = "products"

    id_product: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(7), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    purchase_price: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)
    sale_price: Mapped[float] = mapped_column(DECIMAL(10,4), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    id_category: Mapped[int] = mapped_column(ForeignKey('categories.id_category'), nullable=False)

    def to_json(self) -> dict[str, str]:
        return {
            'id_product': self.id_product,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'brand': self.brand,
            'purchase_price': float(self.purchase_price),
            'sale_price': float(self.sale_price),
            'status': self.status,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'id_category': self.id_category
        }
