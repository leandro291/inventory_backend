from pydantic import BaseModel

class InventorySchema(BaseModel):

    stock: int
    id_product: int
    id_repository: int
