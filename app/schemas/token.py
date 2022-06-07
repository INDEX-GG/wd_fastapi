from pydantic import BaseModel


class AccessToken(BaseModel):
    accessToken: str
    tokenType: str


class GoogleTokenData(BaseModel):
    sub: str
    email: str | None = None
    email_verified: bool = False
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None


class AppleTokenData(BaseModel):
    sub: str
    email: str | None = None
