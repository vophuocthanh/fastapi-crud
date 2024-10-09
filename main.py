from typing import Optional, Union
from prisma import Prisma
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CreatePost(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

@app.get("/")
def list_posts():
    db = Prisma()
    db.connect()
    posts = db.post.find_many()
    db.disconnect()
    return posts


@app.get("/{id}")
def get_post(id: str):
    db = Prisma()
    db.connect()
    post = db.post.find_first(
        where={"id": id}
    )
    db.disconnect()
    return post

@app.post("/")
def create_post(dto: CreatePost):
    db = Prisma()
    db.connect()
    post = db.post.create(
        data=dto.model_dump(exclude_unset=True)
    )
    db.disconnect()
    return post

@app.put("/{id}")
def update_post(id: int, dto: UpdatePost):
    db = Prisma()
    db.connect()
    post = db.post.update(
        where={"id": id},
        data=dto.model_dump(exclude_unset=True)
    )
    db.disconnect()
    return post


@app.delete("/{id}")
def delete_post(id: str):
    db = Prisma()
    db.connect()
    post = db.post.delete(
        where={"id": id}
    )
    db.disconnect()
    return post