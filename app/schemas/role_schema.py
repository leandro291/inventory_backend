from pydantic import BaseModel

class RoleSchema(BaseModel):

    name: str
    description: str