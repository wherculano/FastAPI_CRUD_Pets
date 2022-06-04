from typing import Optional

from pydantic import BaseModel


class PetBase(BaseModel):
    name: str
    kind: str
    breed: str


class PetCreate(PetBase):
    ...

class PetUpdate(PetBase):
    name: Optional[str]
    kind: Optional[str]
    breed: Optional[str]

    
class Pet(PetBase):
    id: int

    class Config:
        orm_mode = True
        
