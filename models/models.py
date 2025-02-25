from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from dbconfiguration.dbconfig import Base
from datetime import datetime
import enum

# Enum for UserType
class UserTypeEnum(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    standard = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fathername = Column(String, nullable=False)
    mothername = Column(String, nullable=False)

    # One-to-One relationship with Profile
    profile = relationship("Profile", uselist=False, back_populates="user")

# Profile Model (Fixed)
class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)  # Add Primary Key
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # ForeignKey reference to User
    user_type = Column(Enum(UserTypeEnum), nullable=False)  # Fix Enum usage
    bloodgroup = Column(String, nullable=True)  # Fix `Colums` to `Column`
    adhar_number = Column(String, nullable=True)  # Fix `Colums` to `Column`

    # Relationship back to User
    user = relationship("User", back_populates="profile")

# Fee Structure Model
class FeeStructure(Base):
    __tablename__ = "fee_structure"

    id = Column(Integer, primary_key=True, index=True)  
    class_number = Column(Integer, nullable=False) 
    fees = Column(Integer, nullable=False)  
    starting_date = Column(DateTime, default=datetime.utcnow)  
    last_date = Column(DateTime, nullable=True)  
    late_fees = Column(Integer, nullable=True)
    discount = Column(Integer, nullable=True)


class Transection_status(str, enum.Enum):
    PENDING="pending"
    SUCESS="sucess"
    FAILED="failed"

class Transection(Base):
    __tablename__="transection"
    id = Column(Integer, primary_key=True, index=True) 
    transection_discription=Column(String, nullable=True)
    transection_date=Column(DateTime, default=datetime.utcnow)
    transection_status=Column(Enum(Transection_status),nullable=False)

class Kota(Base):
    __tablename__="Kota"
    id=Column(Integer, primary_key=True, index=True) 
    kotaname=Column(String,primary_key=False)
    discount=Column(Integer,nullable=False,default=0)
    kotadiscription=Column(String,nullable=True)
