from pydantic import BaseModel
from app.schemas.movement_detail_schema import MovementDetailSchema

class MovementSchema(BaseModel):

    observation: str | None = None
    id_supplier: int
    id_type_movement: int
    id_user: int
    id_repository: int
    movement_details: list[MovementDetailSchema]