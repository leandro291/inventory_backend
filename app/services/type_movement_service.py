from db import db
from app.models.type_movement_model import TypeMovement
from app.schemas.type_movement_schema import TypeMovementSchema

class TypeMovementService:

    def get_all(self) -> list[TypeMovement]:
        type_movements = TypeMovement.query.filter_by(status=True).all()
        return type_movements

    def get_by_name(self, name: str) -> TypeMovement | None:
        type_movement = TypeMovement.query.filter_by(name=name).first()
        return type_movement

    def get_by_id(self, id_type_movement: int) -> TypeMovement | None:
        type_movement = TypeMovement.query.filter_by(id_type_movement=id_type_movement).first()
        return type_movement

    def create(self, data: TypeMovementSchema) -> TypeMovement:

        create_type_movement = TypeMovement(
            name=data.name,
            description=data.description
        )

        db.session.add(create_type_movement)
        db.session.commit()

        return create_type_movement

    def update(self, type_movement: TypeMovement, data: TypeMovementSchema) -> TypeMovement:

        type_movement.name = data.name
        type_movement.description = data.description

        db.session.commit()

        return type_movement

    def delete(self, type_movement: TypeMovement) -> TypeMovement:

        type_movement.status = False
        db.session.commit()

        return type_movement

type_movement_service = TypeMovementService()
