from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.user import router as user
from routes.auth import router as auth

app = FastAPI(
    title='Petship API'
)

app.include_router(user)
app.include_router(auth)
