from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from . import schemas
from . import models
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

posts_data = [{'title': 'title of post1', 'content': 'content of post 1', 'id': 1},
              {'title': 'title of post2', 'content': 'content of post 2', 'id': 2},
              {'title': 'best footballer in the world', 'content': 'CR7', 'id': 3}]


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


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts" ORDER BY created_at DESC """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts/", response_model=schemas.PostResponse)
def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO "Posts" (title, content, published) VALUES
    # (%s, %s, %s) RETURNING *;""", (new_post.title, new_post.content, new_post.published))
    # POST = cursor.fetchone()
    # conn.commit()
    POST = models.Post(**new_post.dict())  # name=new_post.title, content=new_post.content, published=new_post.published
    db.add(POST)
    db.commit()
    db.refresh(POST)
    return POST


@app.get("/posts/{id}")
def getPost(id: int, db: Session = Depends(get_db)):
    # for i in posts_data:
    #     if i['id'] == int(id):
    #         return {'post': i}

    # cursor.execute(""" SELECT * FROM "Posts" WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} does not exists")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM "Posts" WHERE id = %s RETURNING *;""", (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)
    if post_q.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} does not exists")

    post_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE "Posts" SET title = %s, content = %s, published = %s
    # WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    # updated = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    if post1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id = {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
