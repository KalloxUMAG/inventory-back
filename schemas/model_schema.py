from pydantic import BaseModel
from typing import Optional

class ModelSchema(BaseModel):
    id: Optional[int]
    model: str
    brand: str
    product_number: Optional[int]

    class Config:
        orm_mode = True