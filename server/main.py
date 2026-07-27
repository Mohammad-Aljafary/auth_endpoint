
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client
import os

load_dotenv()

supabase_client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}