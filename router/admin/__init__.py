from fastapi import APIRouter
from .filter import router as router_filter

router = APIRouter()


# Include the createprofile router
router.include_router(router_filter, prefix="/admin")