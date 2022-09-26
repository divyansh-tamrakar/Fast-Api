from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, database, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter


router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def loginUser(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    if not utils.verify_user(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
