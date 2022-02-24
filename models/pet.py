from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Pet(BaseModel):
    id: Optional[str] = Field(alias='_id')
    owner: str
    name: str
    type: str
    gender: str
    race: str
    weight: float
    image: Optional[str]
    birthday: datetime