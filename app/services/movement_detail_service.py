from db import db
from app.models.movement_detail_model import MovementDetail
from app.schemas.movement_detail_schema import MovementDetailSchema

class MovementDetailService:

    def get_all(self, id_movement: int) -> list[MovementDetail]:
        details = MovementDetail.query.filter_by(
            id_movement=id_movement
        ).all()
        return details

    def create(self, item: MovementDetailSchema, id_movement: int) -> MovementDetail:
        detail = MovementDetail(
            quantity=item.quantity,
            unit_price=item.unit_price,
            id_product=item.id_product,
            id_movement=id_movement,
        )
        db.session.add(detail)
        return detail


movement_detail_service = MovementDetailService()
