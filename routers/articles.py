from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    description: Optional[str] = None
    author: str
    body: str
    price: Optional[float] = None

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description: "Not found}},
)

# get all articles
@router.get("/")
def get_all_article():
    return {"articles": "all articles"}


# get an article based on id
@router.get("/") # this will retrieve using query parameters
@router.get("/{articleId}") # this will retrieve using path
def get_one_article(articleId: int):
    return {"articles": "one of the articles"}


# delete an article on id
@router.delete("/")
@router.delete("/{article_id}")
def delete_one_article(article_id):
    return {"articles": "articles" + article_id + "deleted successfully"}


# create a new article
@router.post("/")
async def create_article(article: Article):
    article_dict = article.dict()
    if article.title:
        upper_title = article.title.upper()
        article_dict.update({"upper_title": upper_title})
    return article_dict



# update an article
# @router.put("/")
# @router.put("/{articleId}")
# def update_article(articleId: int, body: dict):
#     return {"articles": "articleId=articleId, articleJson=body"}

# update an article
@router.put("/{article_id}")
async def create_item(article_id: int, article: Article): # you can declare path parameters and request JSON body
    return {"article_id": article_id, **article.dict(), "price": "$" + str(article.price)}











