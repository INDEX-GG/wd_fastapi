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
