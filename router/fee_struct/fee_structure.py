from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import FeeStructure ,User,Kota# Import Models
from schemas.schemas import FeeStructureBase,ShowFeeRequest,KotaCreate  # Import Schema
from dependencies import get_db 

router = APIRouter()


@router.post("/Fee_create/", response_model=FeeStructureBase)
def create_fee_structure(fee_data:FeeStructureBase ,db: Session = Depends(get_db)):
        print(fee_data)
        db_fee = FeeStructure(
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
@router.post("/show_Fee/")
def show_fee(user:ShowFeeRequest,db:Session=Depends(get_db)):
        user=db.query(User).filter(User.id==user.user_id).first()
        standard=user.standard
        print(standard)
        feestruct=db.query(FeeStructure).filter(FeeStructure.class_number==int(standard)).first()
        return feestruct

@router.post("/create_kota")
def Create_kota(kota:KotaCreate,db:Session=Depends(get_db)):
        inskota=Kota(kotaname=kota.kotaname,discount=kota.discount,kotadiscription=kota.kotadiscription)
        db.add(inskota)
        db.commit()
        db.refresh(inskota)
        return inskota