from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship,validates
from dbconfiguration.dbconfig import Base
from datetime import datetime
import enum

# Enum for UserType
class UserTypeEnum(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class Transection_status(str, enum.Enum):
    PENDING="pending"
    SUCESS="sucess"
    FAILED="failed"
class Fee_status(str, enum.Enum):
    pending="pending"
    paid="paid"
    late="late"

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
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False) # ForeignKey reference to User
    current_fees_id=Column(Integer,ForeignKey("fee_structure.id"),unique=True,nullable=True) 
    kota_id=Column(Integer,ForeignKey("Kota.id"),unique=True,nullable=True)
    user_type = Column(Enum(UserTypeEnum), nullable=False)  # Fix Enum usage
    bloodgroup = Column(String, nullable=True)  # Fix `Colums` to `Column` 
    adhar_number = Column(String, nullable=True)  # Fix `Colums` to `Column`
    age = Column(Integer, nullable=True) 
    address = Column(String, nullable=True)  # Fix `Colums` to `Column`
    city = Column(String, nullable=True)  # Fix `Colums` to `Column`
    state = Column(String, nullable=True)  # Fix `Colums` to `Column`
    country = Column(String, nullable=True)  # Fix `Colums` to `Column`
    pincode = Column(String, nullable=True)  # Fix `Colums` to `Column`
    fee_status=Column(Enum(Fee_status), nullable=True) 
    # Store image path locally instead of binary data
    profile_image = Column(String, nullable=True)  # Stores path like "static/profile_images/user_123.jpg"
    left_fees=Column(Integer,nullable=True)
    user = relationship("User", back_populates="profile")
    kota=relationship("Kota", back_populates="profile")

    current_fees = relationship("FeeStructure", back_populates="profile")
    


    @validates("birth_year")
    def calculate_age(self, key, birth_year):
        if birth_year:
            current_year = datetime.now().year
            self.age = current_year - birth_year
        return birth_year

    @property
    def calculate_left_fees(self):
        if not self.current_fees:
            return 0
        
        current_date = datetime.utcnow()
        base_fees = self.current_fees.fees
        total_fees = base_fees

        # Calculate late fees if past last date
        if self.current_fees.last_date and current_date > self.current_fees.last_date:
            days_late = (current_date - self.current_fees.last_date).days
            if self.current_fees.late_fees:
                total_fees += (days_late * self.current_fees.late_fees)

        # Apply fee structure discount if available
        if self.current_fees.discount:
            discount_amount = (total_fees * self.current_fees.discount) / 100
            total_fees -= discount_amount

        # Apply Kota discount if available
        if self.kota and self.kota.discount:
            kota_discount = (total_fees * self.kota.discount) / 100
            total_fees -= kota_discount

        self.left_fees = total_fees
        return total_fees

    @validates('current_fees_id')
    def update_left_fees(self, key, value):
        # Update left_fees whenever current_fees_id changes
        if value:
            self.calculate_left_fees
        return value


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
    profile = relationship("Profile", back_populates="current_fees")




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
    profile=relationship("Profile", back_populates="kota")
