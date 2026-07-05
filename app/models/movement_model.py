from db import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, Boolean, DateTime, func, ForeignKey

class Movement(db.Model):
    
    __tablename__ = "movements"

    id_movement: Mapped[int] = mapped_column(Integer, primary_key=True)
    observation: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    id_supplier: Mapped[int] = mapped_column(ForeignKey('suppliers.id_supplier'), nullable=False)
    id_type_movement: Mapped[int] = mapped_column(ForeignKey('type_movements.id_type_movement'), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id_user'), nullable=False)
    id_repository: Mapped[int] = mapped_column(ForeignKey('repositories.id_repository'), nullable=False)

    movement_details = relationship('MovementDetail')
    supplier = relationship('Supplier')
    type_movement = relationship('TypeMovement')
    user = relationship('User')
    repository = relationship('Repository')

    def to_json(self):

        items = []
        for movement_detail in self.movement_details:
            items.append({
                'id_movement_detail': movement_detail.id_movement_detail,
                'quantity': movement_detail.quantity,
                'unit_price': float(movement_detail.unit_price),
                'product': {
                    'id_product': movement_detail.product.id_product,
                    'code': movement_detail.product.code,
                    'name': movement_detail.product.name,
                    'purchase_price': float(movement_detail.product.purchase_price),
                    'sale_price': float(movement_detail.product.sale_price)
                }
            })

        return {
            'id_movement': self.id_movement,
            'observation': self.observation,
            'status': self.status,
            'created_at': str(self.created_at),
            'supplier': self.supplier.to_json(),
            'type_movement': self.type_movement.to_json(),
            'user': self.user.to_json(),
            'repository': self.repository.to_json(),
            'details': items,
        }
