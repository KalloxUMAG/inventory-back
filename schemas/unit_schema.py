from pydantic import BaseModel
from typing import Optional

class UnitSchema(BaseModel):
        id: Optional[int]
        name: str
        building_id: int

        class Config:
                orm_mode = True