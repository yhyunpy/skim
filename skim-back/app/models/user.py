from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRes(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
