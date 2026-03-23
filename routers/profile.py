from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from dependencies.get_current_user import get_current_user
from schemas.profile import ProfileResponse, ProfileUpdate, PublicProfileResponse
from services.profile import get_specific_user, update_my_profile

router = APIRouter()
security = HTTPBearer()


@router.get("/me", response_model=ProfileResponse)
def get_current_profile(
    current_user=Depends(get_current_user), token=Depends(security)
):
    return current_user


@router.patch("/me", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdate, current_user=Depends(get_current_user), token=Depends(security)
):
    return update_my_profile(current_user=current_user, data=data)


@router.get("/{user_id}", response_model=PublicProfileResponse)
def get_user(
    user_id: UUID, current_user=Depends(get_current_user), token=Depends(security)
):
    return get_specific_user(user_id)
