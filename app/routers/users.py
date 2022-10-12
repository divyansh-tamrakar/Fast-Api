from typing import List
from typing import Optional
from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..oauth2 import get_current_user
# from .auth import logoutUser


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=List[schemas.UserResponse])
def getUsers(db: Session = Depends(get_db), search: Optional[str] = "", current_user: int = Depends(get_current_user)):
    users = db.query(models.User).filter(models.User.email.contains(search)).all()
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db), search: Optional[str] = "", current_user: int = Depends(get_current_user)):
    user_q = db.query(models.User).filter(models.User.id == id, models.User.email.contains(search)).first()
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
def deleteUser(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not allowed")
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no such user exists")
    user_query.delete(synchronize_session=False)
    # logoutUser(id)
    db.commit()
    return user
