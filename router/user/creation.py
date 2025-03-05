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
    
    return {"user_id":db_user.id,"acess_token":acess_token,"response":db_user}


@router.post("/login/")
def login_user(user: schemas.UserLogin,db: Session = Depends(get_db)):
    print(user,"user")
    if user.username:
        response=db.query(User).filter(User.username == user.username).first()
    elif user.email:
        response=db.query(User).filter(User.email==user.email).first()
    else:
        raise HTTPException(status_code=400, detail="Either username or email must be provided.")
    if not response:
        return {"message":"user not found"}
    check_password=hashed.verify_password(user.password,response.password)
    if not check_password:
        raise HTTPException(status_code=400, detail="Invalid password.")
    
    else:
        print(response,"response")
        acess_token=token.create_access_token({"email":response.email})
    return {"user_id":response.id,"acess_token":acess_token}
    