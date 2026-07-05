from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, DateTime, func, ForeignKey

class Inventory(db.Model):
    
    __tablename__ = "inventories"

    id_inventory: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    id_product: Mapped[int] = mapped_column(ForeignKey('products.id_product'), nullable=False)
    id_repository: Mapped[int] = mapped_column(ForeignKey('repositories.id_repository'), nullable=False)

    def to_json(self):
        return {
            'id_inventory': self.id_inventory,
            'stock': self.stock,
            'id_product': self.id_product,
            'id_repository': self.id_repository,
            'is_active': self.is_active,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }
