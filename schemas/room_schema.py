from pydantic import BaseModel
from typing import Optional

class RoomSchema(BaseModel):
        id: Optional[int]
        name: str
        unit_id: int

        class Config:
                orm_mode = True