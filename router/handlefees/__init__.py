from fastapi import APIRouter
from .createprofile import router as create_profile_router

router = APIRouter()

# Include the createprofile router
router.include_router(create_profile_router, prefix="/profile")
