from pydantic import BaseModel


class RequestGoogleData(BaseModel):
    token: str


class VkDataDict(BaseModel):
    uid: int
    first_name: str
    last_name: str
    photo: str
    hash: str


class RequestVkData(BaseModel):
    auth_data: VkDataDict


class AppleName(BaseModel):
    firstName: str | None = None
    lastName: str | None = None


class AppleUser(BaseModel):
    email: str | None = None
    name: AppleName | None = None


class RequestAppleData(BaseModel):
    id_token: str
    user: AppleUser | None = None
