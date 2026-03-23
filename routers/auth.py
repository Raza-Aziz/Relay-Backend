from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from dependencies.get_current_user import get_current_user

router = APIRouter()
security = HTTPBearer()


@router.get("/test-auth")
def test_auth(current_user=Depends(get_current_user), token=Depends(security)):
    return current_user
