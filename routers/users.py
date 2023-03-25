from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
# from ..dependencies import get_token_header

class User(BaseModel):
    username: str
    fullname: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    return "fakehash" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def decode_token(token):
    return User(
        username = token + "anydecodestring", email="johndo@email.com", fullname="John Doe"
    )

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)]
)


# get all users
@router.get("/")
def get_all_users():
    return {"Users": "All users we have"}


# get a user based on user id
@router.get("/{user_id}")
def get_one_user(user_id):
    return {"user id": int(user_id)}



