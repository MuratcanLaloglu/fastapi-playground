from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None

@app.get("/")
def root():
    return {"message": "This is my API"}


@app.get("/posts")
def get_posts():
    return {"posts": "This is a post"}

@app.post("/createposts")
def create_post(post: Post):
    print(post.model_dump())
    return {"data": post}