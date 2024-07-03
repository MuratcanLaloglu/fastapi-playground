from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="2534",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("database connection is succesfull")
except Exception as error:
    print("Database connection is failed")
    print(f"Error: {error}")


my_posts: list[dict] = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


def find_post(id: int) -> dict | None:
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


def find_index_post(id: int) -> int | None:
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None


@app.get("/")
def root() -> dict:
    return {"message": "This is my API"}


@app.get("/posts")
def get_posts() -> dict:
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> dict:
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int) -> dict:
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
