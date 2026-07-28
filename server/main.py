
from fastapi import FastAPI

try:
    from .auth_routers.auth_router import router as auth_router
except ImportError:
    from auth_routers.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
