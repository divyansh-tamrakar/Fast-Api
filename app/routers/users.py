from typing import List
from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=List[schemas.UserResponse])
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    user_q = db.query(models.User).filter(models.User.id == id).first()
    if not user_q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id : {id} does not exists")
    return user_q


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"user couldn't be created, try with a different email id")

    return new_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no such user exists")
    user_query.delete(synchronize_session=False)
    db.commit()
    return user
