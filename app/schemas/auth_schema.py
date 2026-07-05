from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):

    name: str
    last_name: str
    email: EmailStr
    password: str
    id_role: int