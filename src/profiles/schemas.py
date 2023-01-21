from pydantic import BaseModel


class ProfileSchema(BaseModel):
    user_id: int

    class Config:
        orm_mode = True
