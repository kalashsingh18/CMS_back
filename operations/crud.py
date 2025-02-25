from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from special import token
from fastapi import FastAPI, Depends, HTTPException
def login_user(db: Session, user: schemas.UserLogin):
    response=db.query(models.User).filter(models.User.username == user.username, models.User.email==user.email).first()
    if not response:
        print("nothing")
    else:
        acess_token=token.create_access_token({"email":response.email})
    return {"id":response.id,"acess_token":acess_token}


def signup(db:Session,user:schemas.Usercreate):
    db_user = models.User(username=user.username, password=user.password,firstname=user.firstname,lastname=user.lastname,standard=user.standard,email=user.email,fathername=user.fathername,mothername=user.mothername)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    acess_token=token.create_access_token({"email":db_user.email})
    
    return {"message":"user created sucessfully","acess_token":acess_token}


def create_fee_structure(db: Session, fee_data:schemas.FeeStructureBase ):
        print(fee_data)
        db_fee = models.FeeStructure(
        class_number=fee_data.class_number,
        fees=fee_data.fees,
        starting_date=fee_data.starting_date,
        last_date=fee_data.last_date,
        late_fees=fee_data.late_fees,
        discount=fee_data.discount
        )
        db.add(db_fee)  
        db.commit()
        db.refresh(db_fee)
        return db_fee  
def create_profile(profile_data: schemas.ProfileCreate, db):
    # Check if the user exists
    user = db.query(models.User).filter(models.User.id == profile_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if a profile already exists for this user
    existing_profile = db.query(models.Profile).filter(models.Profile.user_id == profile_data.user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")

    # Create new profile
    new_profile = models.Profile(
        user_id=profile_data.user_id,
        user_type=profile_data.user_type,
        bloodgroup=profile_data.bloodgroup,
        adhar_number=profile_data.adhar_number
    )

    # Add to database and commit
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile
