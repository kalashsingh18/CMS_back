from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal
import enum
class UserTypeEnum(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
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
    user_id: int
    user_type: UserTypeEnum
    bloodgroup: Optional[str] = None
    adhar_number: Optional[str] = None


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