from fastapi import APIRouter, Response, status 
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()

@router.get('/users', response_model=list[User], tags=["users"])
def find_all():
    return usersEntity(conn.local.user.find())

@router.get('/users/{id}', response_model=User, tags=["users"])
def find_one(id: str):
    user = conn.local.user.find_one({ '_id': ObjectId(id) })
    return userEntity(user)

@router.post('/users', response_model=User, tags=["users"])
def create(user: User):
    user.encrypt_password()
    new_user = dict(user)
    del new_user['id']
    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({ '_id': id })
    return userEntity(user)

@router.put('/users/{id}', response_model=User, tags=["users"])
def update(id: str, user: User):
    conn.local.user.find_one_and_update({ '_id': ObjectId(id) }, { '$set': dict(user) })
    user = conn.local.user.find_one({ '_id': ObjectId(id) })
    return userEntity(user)

@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete(id: str):
    userEntity(conn.local.user.find_one_and_delete({ '_id': ObjectId(id) }))
    return Response(status_code=HTTP_204_NO_CONTENT)
