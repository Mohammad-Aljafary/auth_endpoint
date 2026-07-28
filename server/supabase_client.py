import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = (
    os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("SUPABASE_PUBLISHABLE_KEY")
    or os.getenv("SUPABASE_KEY")
)
supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_ANON_KEY or SUPABASE_PUBLISHABLE_KEY are required"
    )

supabase_client: Client = create_client(supabase_url, supabase_key)
supabase_admin_client: Client | None = (
    create_client(supabase_url, supabase_service_role_key)
    if supabase_service_role_key
    else None
)
