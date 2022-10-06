from typing import List, Optional
from sqlalchemy import func
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostVotes])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * sFROM "Posts" ORDER BY created_at DESC """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id).\
        group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).\
        all()

    return posts


@router.get("/user-posts", response_model=List[schemas.PostResponse])
def getUsersPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM "Posts" ORDER BY created_at DESC """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", response_model=schemas.PostResponse)
def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO "Posts" (title, content, published) VALUES
    # (%s, %s, %s) RETURNING *;""", (new_post.title, new_post.content, new_post.published))
    # POST = cursor.fetchone()
    # conn.commit()
    POST = models.Post(owner_id=current_user.id, **new_post.dict())
    # name=new_post.title, content=new_post.content, published=new_post.published
    db.add(POST)
    db.commit()
    db.refresh(POST)
    return POST


@router.get("/{id}", response_model=schemas.PostVotes)
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # for i in posts_data:
    #     if i['id'] == int(id):
    #         return {'post': i}

    # cursor.execute(""" SELECT * FROM "Posts" WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id).\
        group_by(models.Post.id).\
        filter(models.Post.id == id).\
        first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM "Posts" WHERE id = %s RETURNING *;""", (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)

    if post_q.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} does not exists")
    if post_q.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    post_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE "Posts" SET title = %s, content = %s, published = %s
    # WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    # updated = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    if post1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id = {id} does not exist")
    if post1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
