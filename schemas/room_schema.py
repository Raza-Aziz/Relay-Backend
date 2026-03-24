from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.profile import PublicProfileResponse

"""
RoomWithMembersResponse inherits from RoomResponse
    — it gets all the room fields for free and just adds members on top. You never repeat the room fields.

profile: Optional[PublicProfileResponse] = None is optional because when you just return a room without members (e.g. POST /rooms response),
    - you use RoomResponse not RoomWithMembersResponse — so no profile join is needed there.

members: List[RoomMemberResponse] = [] defaults to an empty list
    — a room with no members yet returns [] instead of None, which is cleaner for the frontend to handle.
"""


class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    slug: str = Field(..., min_length=1, max_length=20)


class DMCreate(BaseModel):
    target_user_id: UUID


class RoomMemberResponse(BaseModel):
    id: UUID
    room_id: UUID
    user_id: UUID
    role: str
    joined_at: Optional[datetime] = None
    # Profile info from the JOIN — gives frontend the username and avatar
    # without this, user_id is just a UUID the frontend cannot display
    profile: Optional[PublicProfileResponse] = None

    class Config:
        from_attributes = True


class RoomResponse(BaseModel):
    id: UUID
    # Nullable — DM rooms have no name or slug
    name: Optional[str] = None
    slug: Optional[str] = None
    # Comes back from Supabase as a plain string e.g. 'dm' or 'group'
    type: str
    # Nullable — ON DELETE SET NULL means this can be None if creator deleted their account
    created_by: Optional[UUID] = None
    # Nullable — new rooms have no messages yet
    last_message_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoomWithMembersResponse(RoomResponse):
    # Extends RoomResponse — inherits all fields above
    # Adds a list of members, each with their profile info
    members: List[RoomMemberResponse] = []

    class Config:
        from_attributes = True
