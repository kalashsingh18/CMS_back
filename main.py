from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from operations import crud
from models import models
from schemas import schemas
from dbconfiguration import dbconfig
from models import models
from special import token
from midleware.tokenmid import JWTAuthMiddleware
from models import models
from dbconfiguration import dbconfig
from router import profile,user,fee_struct,admin
from dependencies import get_db 
from fastapi.staticfiles import StaticFiles


profile_router =profile.createprofile.router
user_route =user.creation.router
fee_router=fee_struct.fee_structure.router
admin_router=admin.filter.router


app = FastAPI()


app.include_router(profile_router, prefix="/api/v1", tags=["Profile"])
app.include_router(user_route, prefix="/api/v1", tags=["User"])
app.include_router(fee_router, prefix="/api/v1", tags=["fee_structure"])
app.include_router(admin_router, prefix="/api/v1", tags=["admin"])



app.add_middleware(JWTAuthMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
dbconfig.Base.metadata.drop_all(bind=dbconfig.engine)  # Drops all tables
dbconfig.Base.metadata.create_all(bind=dbconfig.engine)  # Recreates all tables





 