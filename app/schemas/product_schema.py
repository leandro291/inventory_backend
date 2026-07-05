from pydantic import BaseModel

class ProductSchema(BaseModel):

    name: str
    description: str
    brand: str
    purchase_price: float
    sale_price: float
    id_category: int
