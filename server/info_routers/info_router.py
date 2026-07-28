from fastapi import APIRouter, status, Depends, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Annotated

router = APIRouter()

@router.get("/public/info", status_code=status.HTTP_200_OK)
async def get_public_info() -> dict:
    return {"message": "Welcome stranger! This info is public."}


def oauth2_scheme(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid Authorization header",
    )

@router.get("/protected/profile", status_code=status.HTTP_200_OK)
async def get_protected_profile(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    # Here you would normally validate the token and retrieve user info
    # For demonstration, we'll just return a mock profile
    return {
        "message": "Welcome back! This info is protected.",
        "user": {
            "id": "12345",
            "email": "user@example.com",
            "name": "John Doe",
        },
    }  



