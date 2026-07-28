from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel
from supabase_auth.errors import AuthApiError
from info_routers.info_router import oauth2_scheme

try:
    from ..supabase_client import supabase_admin_client, supabase_client
except ImportError:
    from supabase_client import supabase_admin_client, supabase_client


class AuthCredentials(BaseModel):
    email: str
    password: str


def auth_error_detail(exc: AuthApiError) -> str:
    return exc.message or str(exc) or "Supabase auth request failed"


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={403: {"description": "unauthorized access"}},
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(credentials: AuthCredentials) -> dict:
    if supabase_admin_client is not None:
        try:
            user_response = supabase_admin_client.auth.admin.create_user(
                {
                    "email": credentials.email,
                    "password": credentials.password,
                    "email_confirm": True,
                }
            )
        except AuthApiError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=auth_error_detail(exc),
            ) from exc

        return {
            "message": "User signed up successfully",
            "email": user_response.user.email,
            "id": user_response.user.id,
        }

    try:
        auth_response = supabase_client.auth.sign_up(
            {"email": credentials.email, "password": credentials.password}
        )
    except AuthApiError as exc:
        detail = auth_error_detail(exc)
        if "rate limit" in detail.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Supabase email rate limit exceeded. Add "
                    "SUPABASE_SERVICE_ROLE_KEY to server/.env to create confirmed "
                    "users without sending confirmation emails."
                ),
            ) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc

    if auth_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to sign up user",
        )

    return {
        "message": "User signed up successfully",
        "email": auth_response.user.email,
        "id": auth_response.user.id,
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: AuthCredentials) -> dict:
    try:
        auth_response = supabase_client.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        ) from exc

    if auth_response.session is None or auth_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    return {
        "jwt": auth_response.session.access_token,
        "refresh_token": auth_response.session.refresh_token,
        "user": auth_response.user.model_dump(mode="json"),
        "message": "User logged in successfully",
        "email": auth_response.user.email,
        "id": auth_response.user.id,
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request) -> None:
    oauth2_scheme(request)

    try:
        supabase_client.auth.sign_out()
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) 
