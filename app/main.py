from fastapi import FastAPI
from app.api.users.views import router as user_router
from app.api.skills.views import router as skill_router
from app.auth.views import router as auth_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(skill_router, prefix="/skills", tags=["Skills"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
def read_root() -> dict:
    return {"message": "qwe, FastAPI!"}
