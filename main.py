from curses.ascii import HT
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Pet(BaseModel):
    id: int
    name: str
    kind: str
    breed: str



PETS_LIST = [
    {'id': 1, 'name': 'Lyla', "kind": "dog", "breed": "mutt"},
    {'id': 2, 'name': 'Pantera', "kind": "dog", "breed": "hotweiler"},
    {'id': 3, 'name': 'Willy', "kind": "dog", "breed": "yorkshire"}
]

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
