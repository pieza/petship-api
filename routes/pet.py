from fastapi import APIRouter, Response, Depends, status 
from config.db import db
from config.security.jwt_bearer import JWTBearer
from schemas.pet import petEntity, petsEntity
from models.pet import Pet
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()

@router.get('/pets', dependencies=[Depends(JWTBearer())], response_model=list[Pet], tags=["pets"])
def find(query: dict = {}):
    return petsEntity(db.pet.find(query))

@router.get('/pets/{_id}', dependencies=[Depends(JWTBearer())], response_model=Pet, tags=["pets"])
def find_one(_id: str):
    pet = db.pet.find_one({ '_id': ObjectId(_id) })
    return petEntity(pet)

@router.post('/pets', dependencies=[Depends(JWTBearer())], response_model=Pet, tags=["pets"])
def create(pet: Pet):
    new_pet = pet.dict()
    del new_pet['_id']
    _id = db.pet.insert_one(new_pet).inserted_id
    pet = db.pet.find_one({ '_id': _id })
    return petEntity(pet)

@router.put('/pets/{_id}', dependencies=[Depends(JWTBearer())], response_model=Pet, tags=["pets"])
def update(_id: str, pet: Pet):
    db.pet.find_one_and_update({ '_id': ObjectId(_id) }, { '$set': dict(pet) })
    pet = db.pet.find_one({ '_id': ObjectId(_id) })
    return petEntity(pet)

@router.delete('/pets/{_id}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT, tags=["pets"])
def delete(_id: str):
    petEntity(db.pet.find_one_and_delete({ '_id': ObjectId(_id) }))
    return Response(status_code=HTTP_204_NO_CONTENT)