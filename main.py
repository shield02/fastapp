from typing import Annotated

from fastapi import FastAPI, Depends, Header, HTTPException
from routers import users, articles

User = users.User


app = FastAPI()

# include other routers
app.include_router(users.router)
app.include_router(articles.router)

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")





async def get_current_user(token: Annotated[str, Depends()]):
    user = decode_token(token)
    return user


# get authenticated current user
@app.get("/me")
def get_current_auth_user(auth_user: Annotated[User, Depends(get_current_user)]):
    return auth_user.dict()



