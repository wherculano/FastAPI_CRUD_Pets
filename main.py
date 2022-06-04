from typing import List
from http import HTTPStatus

import crud
import models
import schemas
from database import engine, SessionLocal

from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Response


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> None:
    """ Gets dabatase connection """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/pet', response_model=List[schemas.Pet])
async def get_pets(kind: str = None, db: Session = Depends(get_db)) -> List:
    """ Returns a list of pets """
    return crud.get_pets_with_filter(db, kind)


@app.get('/pet/{pet_id}', response_model=schemas.Pet)
async def get_pets(pet_id: int, db: Session = Depends(get_db)) -> List:
    """ Returns a especific pet from a list of pets """

    pet_db = crud.get_pet(db, pet_id)
    
    if pet_db:
        return pet_db
    
    raise HTTPException(status_code=404, detail='Pet not found')


@app.post('/pet', response_model=schemas.Pet, status_code=201)
async def insert_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    """ Inserts a new pet on database """
    return crud.insert_pet(db, pet)


@app.delete('/pet/{pet_id}', status_code=204)
async def delete_pet(pet_id: int, db: Session = Depends(get_db)) -> None:   
    """ Deletes a especific pet from databse """
    pet_db = crud.get_pet(db, pet_id)
    
    if pet_db:
        crud.delete_pet(db, pet_id)
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException(status_code=404, detail='Pet not found') 


@app.patch('/pet/{pet_id}', response_model=schemas.Pet)
async def update_pet(pet_id: int, pet: schemas.PetUpdate, db: Session = Depends(get_db)):
    pet_db = crud.get_pet(db, pet_id)
    
    if pet_db:
        return crud.update_pet(db, pet_id, pet)
    raise HTTPException(status_code=404, detail='Pet not found')
