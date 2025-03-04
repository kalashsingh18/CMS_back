from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from typing import Literal
import enum
class UserTypeEnum(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class Fee_status(str, enum.Enum):
    PAID = "paid"
    PENDING = "pending"
    OVERDUE = "overdue"

class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str 

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    acess_token:str

    class Config:
        orm_mode = True

class Users(BaseModel):
    id: int
    username: str
    email: EmailStr
  

    class Config:
        orm_mode = True
class Usercreate(BaseModel):
    username:str
    firstname:str
    lastname:str
    password:str
    standard:int
    email:EmailStr
    fathername:str
    mothername:str

class ProfileCreate(BaseModel):
    user_type: UserTypeEnum
    user_id:int
    bloodgroup: Optional[str] = None
    age: Optional[int] = None
  
    
    adhar_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    profile_image: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    user_type: UserTypeEnum
    bloodgroup: Optional[str] = None
    adhar_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    profile_image: Optional[str] = None
    fee_status: Optional[Fee_status] = None
    left_fees: Optional[int] = None

    class Config:
        from_attributes = True



class FeeStructureBase(BaseModel):
    class_number: int
    fees: Optional[int] = None
    starting_date: Optional[datetime] = None
    last_date: Optional[datetime] = None
    late_fees: Optional[int] = None
    discount: Optional[int] = None

class ShowFeeRequest(BaseModel):
    user_id: int

class fiter_standard_fee(BaseModel):
  standard_value:int

class KotaBase(BaseModel):
    kotaname: str = Field(..., example="Premium Kota")
    discount: int = Field(0, example=10)
    kotadiscription: Optional[str] = Field(None, example="Special discounted Kota")

class KotaCreate(KotaBase):
    pass


class KotaResponse(KotaBase):
    id: int
