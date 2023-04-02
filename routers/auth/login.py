from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from routers import users
from typing import Annotated

User = users()

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


router = APIRouter(
    prefix="",
    tags=["login"],
    dependencies=[Depends(oauth2_scheme)]
)


def hash_password(password: str):
    return "fakehash" + password


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def decode_token(token):
    user = get_user(users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username and password")

    return {"access_token": user.username, "token_type": "bearer"}


# get authenticated current user
@router.get("/me")
async def get_current_auth_user(
        auth_user: Annotated[User, Depends(get_current_active_user)]
):
    return auth_user




