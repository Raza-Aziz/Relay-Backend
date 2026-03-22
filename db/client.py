import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_SERVICE_KEY == None or SUPABASE_URL == None:
    raise ValueError("Missing Supabase credentials in .env")


client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
