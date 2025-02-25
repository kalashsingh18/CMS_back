from sqlalchemy.orm import Session
from dbconfiguration.dbconfig import SessionLocal  # Your DB session setup

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
