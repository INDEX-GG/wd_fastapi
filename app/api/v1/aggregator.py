from fastapi import APIRouter

from app.api.v1.endpoints import login, users, posts, vacancy, files, favorites, shoutout


api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(posts.router)
api_router.include_router(vacancy.router)
api_router.include_router(files.router)
api_router.include_router(favorites.router)
api_router.include_router(shoutout.router)
