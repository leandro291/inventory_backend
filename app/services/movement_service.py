from db import db
from app.models.movement_model import Movement
from app.schemas.movement_schema import MovementSchema

class MovementService:

    def get_all(self) -> list[Movement]:
        movements = Movement.query.filter_by(status=True).all()
        return movements

    def get_by_id(self, id_movement: int) -> Movement | None:
        movement = Movement.query.filter_by(
            id_movement=id_movement,
            status=True,
        ).first()
        return movement

    def create(self, data: MovementSchema) -> Movement:
        movement = Movement(
            observation=data.observation,
            id_supplier=data.id_supplier,
            id_type_movement=data.id_type_movement,
            id_user=data.id_user,
            id_repository=data.id_repository,
        )
        db.session.add(movement)
        return movement

    def delete(self, movement: Movement) -> Movement:
        movement.status = False
        db.session.commit()
        return movement


movement_service = MovementService()
