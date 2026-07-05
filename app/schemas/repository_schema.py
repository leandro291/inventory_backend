from pydantic import BaseModel

class RepositorySchema(BaseModel):

    name: str
    location: str
