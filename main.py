from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts: list[dict] = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]


@app.get("/")
def root():
    return {"message": "This is my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)   
    return {"data": post_dict}
