from fastapi import APIRouter, Response, Depends, status 
from config.db import db
from config.security.jwt_bearer import JWTBearer
from utils.crypt import encrypt_password, check_password
from schemas.user import userEntity, usersEntity
from models.user import User
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()

@router.get('/users', dependencies=[Depends(JWTBearer())], response_model=list[User], tags=["users"])
def find_all():
    return usersEntity(db.user.find())

@router.get('/users/{id}', dependencies=[Depends(JWTBearer())], response_model=User, tags=["users"])
def find_one(id: str):
    user = db.user.find_one({ '_id': ObjectId(id) })
    return userEntity(user)

@router.post('/users', dependencies=[Depends(JWTBearer())], response_model=User, tags=["users"])
def create(user: User):
    new_user = dict(user)
    new_user['password'] = encrypt_password(new_user['password'])
    del new_user['id']
    id = db.user.insert_one(new_user).inserted_id
    user = db.user.find_one({ '_id': id })
    return userEntity(user)

@router.put('/users/{id}', dependencies=[Depends(JWTBearer())], response_model=User, tags=["users"])
def update(id: str, user: User):
    db.user.find_one_and_update({ '_id': ObjectId(id) }, { '$set': dict(user) })
    user = db.user.find_one({ '_id': ObjectId(id) })
    return userEntity(user)

@router.delete('/users/{id}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete(id: str):
    userEntity(db.user.find_one_and_delete({ '_id': ObjectId(id) }))
    return Response(status_code=HTTP_204_NO_CONTENT)
