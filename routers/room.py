from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from dependencies.get_current_user import get_current_user
from schemas.room_schema import DMCreate, RoomCreate, RoomResponse
from services.room import create_dm_room_service, create_group_room_service

router = APIRouter()
security = HTTPBearer()


@router.post("/", response_model=RoomResponse)
def create_group_room(
    data: RoomCreate, current_user=Depends(get_current_user), token=Depends(security)
):
    return create_group_room_service(data, current_user)


@router.post("/dm", response_model=RoomResponse)
def create_dm_room(
    data: DMCreate, current_user=Depends(get_current_user), token=Depends(security)
):
    return create_dm_room_service(data, current_user)
