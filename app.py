from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.user import router as user

app = FastAPI(
    title='Petship API'
)

app.include_router(user)
