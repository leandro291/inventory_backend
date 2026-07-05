from pydantic import BaseModel

class ProductSchema(BaseModel):

    name: str
    description: str
    brand: str
    purchase_price: float
    sales_price: float
    id_category: int
