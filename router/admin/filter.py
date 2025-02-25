from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import FeeStructure ,User# Import Models
from schemas.schemas import fiter_standard_fee # Import Schema
from dependencies import get_db 

router = APIRouter()
@router.post("/filter/")
def filter_user_fee(standard:fiter_standard_fee ,db: Session = Depends(get_db)):
       result = db.query(User).filter(User.standard == standard.standard_value).all()
       fee=db.query(FeeStructure).filter(FeeStructure.class_number==standard.standard_value).first()
       user_list = [user.__dict__ for user in result]
       for user in user_list:
            user.pop("_sa_instance_state", None)
            user["fee"]=fee.fees
            user["from"]=fee.starting_date
            user["to"]=fee.last_date
            user["late_fees"]=fee.late_fees
            user["given_discount"]=fee.discount
       return user_list
