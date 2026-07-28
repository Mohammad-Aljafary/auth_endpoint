
from fastapi import FastAPI
from auth_routers.auth_router import router as auth_router
from info_routers.info_router import router as info_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(info_router)

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
