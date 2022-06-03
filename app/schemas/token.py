from pydantic import BaseModel


class AccessToken(BaseModel):
    accessToken: str
    tokenType: str
