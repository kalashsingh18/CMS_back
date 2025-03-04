from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Profile, User  # Import Models
from schemas import schemas # Import Schema
from special import token
from dependencies import get_db
from special import hashed

router = APIRouter()

@router.post("/signup/")
def signup(user:schemas.Usercreate,db: Session = Depends(get_db)):
    hashed_password = hashed.hash_password(user.password)
    db_user = User(username=user.username, password=hashed_password,firstname=user.firstname,lastname=user.lastname,standard=user.standard,email=user.email,fathername=user.fathername,mothername=user.mothername)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    acess_token=token.create_access_token({"email":db_user.email})
    
    return {"user_id":db_user.id,"acess_token":acess_token}


@router.post("/login/")
def login_user(user: schemas.UserLogin,db: Session = Depends(get_db)):
    response=db.query(User).filter(User.username == user.username, User.email==user.email).first()
    if not response:
        print("nothing")
    else:
        print(response,"response")
        acess_token=token.create_access_token({"email":response.email})
    return {"user_id":response.id,"acess_token":acess_token}
    