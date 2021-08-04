from fastapi import APIRouter, Body, HTTPException
from models.user import User, UserLogin
from utils.crypt import encrypt_password, check_password
from config.db import db
from config.security.auth import signJWT
from starlette.status import HTTP_400_BAD_REQUEST 

router = APIRouter()

def check_user(data: UserLogin):
    user = db.user.find_one({ 'email': data.email })
    if user is not None and check_password(user['password'], data.password):
        return True
    return False

@router.post('/auth/signup', tags=['auth'])
def signup(user: User):
    if db.user.find_one({ 'email': data.email }) is not None:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='User already exists!')    
    new_user = dict(user)
    new_user['password'] = encrypt_password(new_user['password'])
    del new_user['id']
    id = db.user.insert_one(new_user).inserted_id
    user = db.user.find_one({ '_id': id })
    return signJWT(user['email']) 

@router.post('/auth/login', tags=['auth'])
async def login(user: UserLogin = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Wrong credentials!')
