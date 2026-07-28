from fastapi import APIRouter, status, Depends, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Annotated
try:
    from ..supabase_client import supabase_client
except ImportError:
    from supabase_client import  supabase_client


class UserInfo(BaseModel):
    id: str
    email: str

router = APIRouter()

@router.get("/public/info", status_code=status.HTTP_200_OK)
async def get_public_info() -> dict:
    return {"message": "Welcome stranger! This info is public."}


def oauth2_scheme(request: Request) -> UserInfo:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            response = supabase_client.auth.get_user(auth_header.split(" ")[1])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header",
            )
        user_info = UserInfo(
            id=response.user.id,
            email=response.user.email,
            name=response.user.user_metadata.get("name", ""),
        )
        return user_info
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid Authorization header",
    )

@router.get("/protected/profile", status_code=status.HTTP_200_OK)
async def get_protected_profile(current_user: Annotated[UserInfo, Depends(oauth2_scheme)]) -> dict:
    # Here you would normally validate the token and retrieve user info
    # For demonstration, we'll just return a mock profile
    return {"message": "This is protected profile info.", "user": current_user}  


@router.get("/protected/dashboard", status_code=status.HTTP_200_OK)
async def get_protected_dashboard(current_user: Annotated[UserInfo, Depends(oauth2_scheme)]) -> dict:
    # Here you would normally validate the token and retrieve user info
    # For demonstration, we'll just return a mock dashboard
    return {"message": "This is protected dashboard info.", "user": current_user}  
