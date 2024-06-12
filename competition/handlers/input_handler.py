from pydantic import BaseModel


class InputBase(BaseModel):
    name: str
    type: str
    value: str

class InputCreate(InputBase):
    pass

class Input(InputBase):
    id: int

    class Config:
        orm_mode = True
