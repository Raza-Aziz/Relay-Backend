from fastapi import FastAPI
from fastapi.security import HTTPBearer

from db.client import client
from routers import auth, profile, room

security = HTTPBearer()

app = FastAPI()


@app.get("/tables")
def get_all_tables():
    try:
        profiles = client.table("profile").select("*").limit(1).execute()
        rooms = client.table("room").select("*").limit(1).execute()
        room_members = client.table("room_member").select("*").limit(1).execute()
        messages = client.table("message").select("*").limit(1).execute()

        return {
            "profiles": profiles.data,
            "rooms": rooms.data,
            "room_members": room_members.data,
            "messages": messages.data,
        }
    except Exception as e:
        print(f"An error occurred {e}")


@app.get("/health")
def check_health():
    try:
        result = client.table("profile").select("*").limit(1).execute()
        rows = result.data
        return rows
    except Exception as e:
        print(f"An error occurred {e}")


app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api/profile")
app.include_router(room.router, prefix="/api/rooms")
