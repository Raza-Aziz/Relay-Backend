import re

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from db.client import client
from schemas.room_schema import DMCreate, RoomCreate


def create_group_room_service(data: RoomCreate, current_user):
    pattern = re.compile("^[a-z0-9-]+$")
    if not pattern.match(data.slug):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Slug can only contain lowercase letters, numbers, and hyphens",
        )

    # Check slug uniqueness
    result = client.table("room").select("*").eq("slug", data.slug).execute()
    if result.data:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Slug already taken")

    # Step 3 - Insert room in 'room' table
    room_response = (
        client.table("room")
        .insert(
            {
                "name": data.name,
                "slug": data.slug,
                "type": "group",
                "created_by": current_user["id"],
            }
        )
        .execute()
    )

    # Step 4 - Get room info
    new_room = room_response.data[0]

    # Step 5 - Insert room member in 'room_member' table
    new_room_member = (
        client.table("room_member")
        .insert(
            {
                "room_id": new_room["id"],
                "user_id": current_user["id"],
                "role": "admin",
            }
        )
        .execute()
    )

    # Step 6 - Return room info
    return new_room


def create_dm_room_service(data: DMCreate, current_user):
    # check if target user is not current user
    if str(data.target_user_id) == str(current_user["id"]):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Cannot DM yourself"
        )

    # query if user exists
    target_user = (
        client.table("profile").select("*").eq("id", data.target_user_id).execute()
    )

    if not target_user.data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    # Check if rooms already exist for current user
    my_dms = (
        client.table("room_member")
        .select("room_id, room!inner(*)")  # Ensure it joins with room & filters by DM
        .eq("user_id", current_user["id"])
        .execute()
    )

    my_dm_room_ids = [
        row["room_id"] for row in my_dms.data if row["room"]["type"] == "dm"
    ]

    # if they exist
    if my_dm_room_ids:
        # then should check if the type is dm and other user is target user
        existing_dm_room = (
            client.table("room_member")
            .select("room_id")
            .eq("user_id", data.target_user_id)
            .in_("room_id", my_dm_room_ids)
            .execute()
        )

        if existing_dm_room.data:
            existing_dm_room_id = existing_dm_room.data[0]["room_id"]
            room = (
                client.table("room").select("*").eq("id", existing_dm_room_id).execute()
            )

            return room.data[0]

    new_dm_room = client.table("room").insert({"type": "dm"}).execute()

    new_dm_room_id = new_dm_room.data[0]["id"]

    new_dm_room_member_1 = (
        client.table("room_member")
        .insert(
            {
                "room_id": new_dm_room_id,
                "user_id": str(current_user["id"]),
                "role": "member",
            }
        )
        .execute()
    )

    new_dm_room_member_2 = (
        client.table("room_member")
        .insert(
            {
                "room_id": new_dm_room_id,
                "user_id": str(data.target_user_id),
                "role": "member",
            }
        )
        .execute()
    )

    return new_dm_room.data[0]
