from fastapi import APIRouter
from .fee_structure import router as router_fee_struct

router = APIRouter()
print("test")

# Include the createprofile router
router.include_router(router_fee_struct, prefix="/fee_struct")