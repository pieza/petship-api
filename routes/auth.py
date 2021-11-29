from fastapi import APIRouter, Body, Depends, HTTPException
from bson.objectid import ObjectId
from models.user import User, UserLogin
from schemas.user import userEntity, usersEntity
from utils.crypt import encrypt_password, check_password
from config.db import db
from config.security.auth import signJWT, decodeJWT
from config.security.jwt_bearer import JWTBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

router = APIRouter()

async def get_current_user(token: str = Depends(JWTBearer())):
    decoded_token = decodeJWT(token)
    user = db.user.find_one(ObjectId(decoded_token['user_id']))
    return userEntity(user)

@router.post('/auth/signup', response_model=User, tags=['auth'])
def signup(user: User):
    if db.user.find_one({ 'email': user.email }) is not None:
        return HTTPException(status_code=HTTP_409_CONFLICT, detail='User already exists!')    
    new_user = dict(user)
    new_user['password'] = encrypt_password(new_user['password'])
    _id = db.user.insert_one(new_user).inserted_id
    user = db.user.find_one(_id)
    return userEntity(user)

@router.post('/auth/login', tags=['auth'])
async def login(data: UserLogin = Body(...)):
    user = db.user.find_one({ 'email': data.email })
    if user is not None and check_password(user['password'], data.password):
        return signJWT(str(user['_id']))
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Wrong credentials!')

@router.get('/auth/current', response_model=User, tags=['auth'])
def current(current_user: User = Depends(get_current_user)):
    return userEntity(current_user)