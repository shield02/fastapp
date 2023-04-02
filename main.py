from typing import Annotated

from fastapi import FastAPI, Depends, Header, HTTPException
from routers import auth, users, articles


app = FastAPI()

# include other routers
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(auth.login.router)


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")



