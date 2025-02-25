from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Profile, User  # Import Models
from schemas.schemas import ProfileCreate  # Import Schema
from dependencies import get_db 

# Create APIRouter instance
router = APIRouter()

@router.post("/profile_create/", response_model=ProfileCreate)
def create_profile(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter(User.id == profile_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if a profile already exists for this user
    existing_profile = db.query(Profile).filter(Profile.user_id == profile_data.user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this user")

    # Create new profile
    new_profile = Profile(
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
