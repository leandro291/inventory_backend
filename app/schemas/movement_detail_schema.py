from pydantic import BaseModel

class MovementDetailSchema(BaseModel):

    quantity: int
    unit_price: float
    id_product: int
