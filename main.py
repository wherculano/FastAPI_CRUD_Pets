from curses.ascii import HT
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PetBase(BaseModel):
    name: str
    kind: str
    breed: str


class PetCreate(PetBase):
    ...


class Pet(PetBase):
    id: int

PETS_LIST = [
    {'id': 1, 'name': 'Lyla', "kind": "dog", "breed": "mutt"},
    {'id': 2, 'name': 'Pantera', "kind": "dog", "breed": "hotweiler"},
    {'id': 3, 'name': 'Willy', "kind": "dog", "breed": "yorkshire"}
]

ID_COUNTER = 3

@app.get('/pet', response_model=List[Pet])
async def get_pets(kind: str = None) -> List:
    """ Returns a list of pets """
    
    if kind:
        return [pet for pet in PETS_LIST if pet['kind'] == kind.lower()]
    return PETS_LIST


@app.get('/pet/{pet_id}', response_model=Pet)
async def get_pets(pet_id: int) -> List:
    """ Returns a especific pet from a list of pets """

    for pet in PETS_LIST:
        if pet['id'] == pet_id:
            return pet
    
    if not pet:
        raise HTTPException(status_code=404, detail='Pet not found')
    
    return pet


@app.post('/pet', response_model=Pet)
async def insert_pet(pet: PetCreate):
    global ID_COUNTER
    new_pet = pet.dict()
    new_pet['id'] = ID_COUNTER
    ID_COUNTER += 1

    PETS_LIST.append(new_pet)

    return new_pet
