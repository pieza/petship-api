from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(alias='_id')
    name: str
    email: EmailStr
    password: str
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
