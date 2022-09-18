from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


posts_data = [{'title': 'title of post1', 'content': 'content of post 1', 'id': 1},
              {'title': 'title of post2', 'content': 'content of post 2', 'id': 2},
              {'title': 'best footballer in the world', 'content': 'CR7', 'id': 3}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FASTAPI-Project',
                                user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\n\n----------------------database connection successful----------------------\n\n")
        break
    except Exception as e:
        print("Connection to database failed")
        print(e)
        time.sleep(2)


@app.get("/")
def root():

    return {'message': 'hello'}


@app.get("/test")
def test_post(db : Session = Depends(get_db)):
    return {'message': 'success'}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM "Posts" ORDER BY created_at DESC """)
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/posts/")
def create_post(new_post: Post):
    cursor.execute(""" INSERT INTO "Posts" (title, content, published) VALUES 
    (%s, %s, %s) RETURNING *;""", (new_post.title, new_post.content, new_post.published))
    POST = cursor.fetchone()

    conn.commit()

    return {'data': POST}


@app.get("/posts/{id}")
def getPost(id: int):
    # for i in posts_data:
    #     if i['id'] == int(id):
    #         return {'post': i}

    cursor.execute(""" SELECT * FROM "Posts" WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="post does not exists")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute(""" DELETE FROM "Posts" WHERE id = %s RETURNING *;""", (str(id), ))
    del_post = cursor.fetchone()
    conn.commit()
    if del_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} does not exists")


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def updatePost(id: int, post: Post):
    cursor.execute(""" UPDATE "Posts" SET title = %s, content = %s, published = %s
    WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated = cursor.fetchone()
    conn.commit()
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id = {id} does not exist")
    return {"updated post": updated}
