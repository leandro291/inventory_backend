from pydantic import BaseModel

class CompanySchema(BaseModel):
    name: str
    ruc: str
    address: str
    