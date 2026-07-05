from db import db
from sqlalchemy import Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class MovementDetail(db.Model):

    __tablename__ = 'movement_details'

    id_movement_detail: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(DECIMAL(10, 4), nullable=False)
    id_product: Mapped[int] = mapped_column(ForeignKey('products.id_product'), nullable=False)
    id_movement: Mapped[int] = mapped_column(ForeignKey('movements.id_movement'), nullable=False)

    product = relationship('Product')
