from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
# from ..dependencies import get_token_header

from models import user


User = user.User()

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


# create a new user
@router.post("/create-user")
def create_user(new_user: Annotated[User, Depends()]):
    return new_user


