from pydantic import BaseModel
from typing import Optional

class ModelSchema(BaseModel):
    id: Optional[int]
    name: str
    brand_id: int

    class Config:
        orm_mode = True