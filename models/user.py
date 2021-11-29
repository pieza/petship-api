from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    _id: Optional[str]
    name: str
    email: EmailStr
    password: str
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
