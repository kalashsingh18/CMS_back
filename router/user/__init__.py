from fastapi import APIRouter
from .creation import router as register_router

router = APIRouter()

# Include the createprofile router
router.include_router(register_router, prefix="/register")