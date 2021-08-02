import bcrypt
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str

    def encrypt_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt())
