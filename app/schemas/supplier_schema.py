from pydantic import BaseModel

class SupplierSchema(BaseModel):

    name: str
    email: str
    telephone: str
    id_company: int