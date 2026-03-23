from fastapi import Header, HTTPException, status

from db.client import client


def get_current_user(authorization=Header(None)):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authorization header provided",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format",
        )

    token = authorization.split(" ")[1]

    try:
        result = client.auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if result is None or result.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    uuid = result.user.id

    profile_result = client.table("profile").select("*").eq("id", uuid).execute()

    if profile_result.data is None or profile_result.data == []:
        new_profile = (
            client.table("profile")
            .insert({"id": uuid, "username": result.user.email.split("@")[0]})
            .execute()
        )
        return new_profile.data[0]

        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail="User not found",
        # )

    return profile_result.data[0]
