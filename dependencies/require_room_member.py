from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path
from starlette.status import HTTP_403_FORBIDDEN

from db.client import client
from dependencies.get_current_user import get_current_user


def require_room_member(
    room_id: Annotated[UUID, Path(...)], current_user=Depends(get_current_user)
):
    result_rooms = (
        client.table("room_member")
        .select("*")
        .eq("room_id", str(room_id))
        .eq("user_id", str(current_user["id"]))  # current_user is a dict
    ).execute()

    if not result_rooms.data:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="User not member of this room"
        )

    return result_rooms.data[0]
