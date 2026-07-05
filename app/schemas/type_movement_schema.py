from pydantic import BaseModel

class TypeMovementSchema(BaseModel):

    name: str
    description: str
