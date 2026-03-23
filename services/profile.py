from uuid import UUID

from fastapi import Depends, HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from db.client import client
from dependencies.get_current_user import get_current_user
from schemas.profile import ProfileUpdate


def get_profile(current_user=Depends(get_current_user)):
    result = client.table("profile").select("*").eq("id", current_user["id"]).execute()

    if result.data is None or result.data == []:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Profile not found")

    return result.data[0]


def update_my_profile(current_user: dict, data: ProfileUpdate):
    data_dict = data.model_dump(exclude_unset=True)

    if not data_dict:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    if "avatar_url" in data_dict and data_dict["avatar_url"] is not None:
        data_dict["avatar_url"] = str(data_dict["avatar_url"])

    if "username" in data_dict:
        result = (
            client.table("profile")
            .select("id")
            .eq("username", data_dict["username"])
            .neq("id", current_user["id"])
            .execute()
        )

        if result.data:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail="Username already taken"
            )

    updated_data = (
        client.table("profile").update(data_dict).eq("id", current_user["id"]).execute()
    )

    if not updated_data.data:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Update failed"
        )

    return updated_data.data[0]


def get_specific_user(user_id: UUID):
    result = client.table("profile").select("*").eq("id", user_id).execute()

    if not result.data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return result.data[0]
