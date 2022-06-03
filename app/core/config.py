from typing import List, Dict
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):

    TITLE: str = "string"
    DESCRIPTION: str = "string"
    VERSION: str = "string"
    CONTACTS: Dict[str, str] = {
        "name": "string",
        "url": "string",
    }
    OPENAPI_TAGS: List[Dict[str, str]] = []

    ROOT_PATCH: str = ""
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List[str] = ["*"]
    SQLALCHEMY_DATABASE_URL: str = "string"
    ACCESS_TOKEN_SECRET_KEY: str = "string"
    REFRESH_TOKEN_SECRET_KEY: str = "string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365
    google_Client_ID: str = "string"
    google_Client_Secret: str = "string"
    vk_Secure_Key: str = "string"
    vk_app_id: str = "string"

    class Config:
        case_sensitive = True


settings = Settings()
