from typing import Dict, List, Union

from sqlalchemy.orm import Session

import models
import schemas


def get_pets_with_filter(db: Session, kind: str = None) -> List:
    """ Gets pet from database
    
    Parameters
    ----------
    db: Session
        Database session
    kind: str
        Pet's kind
    
    Returns
    -------
    List
        Pet's information

    """
    if kind:
        return db.query(models.Pet).filter(models.Pet.kind == kind.lower()).all()
    return db.query(models.Pet).all()


def insert_pet(db: Session, pet: schemas.PetCreate) -> models.Pet:
    """ Inserts a new pet on database 
    
    Parameters
    ----------
    db: Session
        Database session
    pet: schemas.PetCreate
        PetCreate type
    
    Returns
    -------
    pet_db: models.Pet
        Pet type

    """
    pet_db = models.Pet(**pet.dict())
    db.add(pet_db)
    db.commit()
    db.refresh(pet_db)
    return pet_db

def get_pet(db: Session, pet_id: int) -> List:
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def delete_pet(db: Session, pet_id: int) -> None:
    db.query(models.Pet).filter(models.Pet.id == pet_id).delete()
    db.commit()

def update_pet(db: Session, pet_id: int, pet: schemas.PetUpdate) -> models.Pet:
    pet_db = get_pet(db, pet_id)
    pet_db.name = pet.name or pet_db.name
    pet_db.kind = pet.kind or pet_db.kind
    pet_db.breed = pet.breed or pet_db.breed

    db.add(pet_db)
    db.commit()
    db.refresh(pet_db)

    return pet_db

