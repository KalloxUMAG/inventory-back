from typing import Optional
from pydantic import BaseModel, validator
from datetime import date
from io import BytesIO
from PIL import Image

class InvoiceSchema(BaseModel):
    id: Optional[int]
    number: int
    date: date
    supplier_id: Optional[int]

    class Config:
        orm_mode = True