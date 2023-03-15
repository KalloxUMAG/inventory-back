from fastapi import APIRouter, Response, File, UploadFile
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from config.database import get_session
from models.models import Invoices
from schemas.invoce_schema import InvoiceSchema
from typing import List
from io import BytesIO
from PIL import Image

invoices = APIRouter()

@invoices.get("/api/invoices", response_model=List[InvoiceSchema])
def get_inovices():
    result = get_session().query(Invoices).all()
    return result

@invoices.post("/api/invoices", status_code=HTTP_201_CREATED)
async def add_invoice(invoice: InvoiceSchema):
    # Crear la compra
    new_invoice = Invoices(number=invoice.number, date=invoice.date)
    session = get_session()
    session.add(new_invoice)
    session.commit()
    content = str(new_invoice.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@invoices.get("/api/invoices/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(invoice_id: int):
    return get_session().query(Invoices).filter(Invoices.id == invoice_id).first()

@invoices.delete("/api/invoices/{invoice_id}", status_code=HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int):
    db_invoice = get_invoice(invoice_id)
    if not db_invoice:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_invoice)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)