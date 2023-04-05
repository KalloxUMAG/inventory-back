from pydantic import BaseModel
from typing import Optional

class ModelNumberSchema(BaseModel):
    id: Optional[int]
    number: str
    model_id: int

    class Config:
        orm_mode = True