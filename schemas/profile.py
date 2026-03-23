import re
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator


class ProfileResponse(BaseModel):
    """
    What you return when showing a user their own profile
    """

    id: UUID
    username: str
    avatar_url: Optional[HttpUrl] = None
    online_status: Optional[str] = None
    last_seen_at: Optional[datetime]
    created_at: Optional[datetime]

    # This tells Pydantic it can read data from a dictionary (which is what Supabase returns),
    #  not just from another Pydantic object.
    class Config:
        from_attributes = True


class PublicProfileResponse(BaseModel):
    """
    What you return when showing someone else's profile
    """

    id: UUID
    username: str
    avatar_url: Optional[HttpUrl] = None
    online_status: Optional[str] = None
    last_seen_at: Optional[datetime]

    # This tells Pydantic it can read data from a dictionary (which is what Supabase returns),
    #  not just from another Pydantic object.
    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    """
    What the user sends when updating their profile
    """

    username: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value):
        # If no username was sent, simply return username
        if value is None:
            return value

        if len(value) < 3:
            raise ValueError("Username must be atleast 3 characters")

        if len(value) > 30:
            raise ValueError("Username must be at most 30 characters")

        # re.match checks if the value matches the pattern from the start
        # ^ means start, [a-zA-Z0-9_] means letters, numbers, underscores only
        # + means one or more characters, $ means end
        # If it does NOT match, the username contains invalid characters
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )

        # If all checks pass, return the value unchanged
        return value
