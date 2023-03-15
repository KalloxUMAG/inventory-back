from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Supplier_contact
from schemas.supplier_contact_schema import SupplierContactSchema
from typing import List

from routes.suppliers import get_supplier

suppliers_contacts = APIRouter()

@suppliers_contacts.get("/api/suppliers_contacts", response_model=List[SupplierContactSchema])
def get_suppliers_contacts():
    result = get_session().query(Supplier_contact).all()
    return result

@suppliers_contacts.post("/api/suppliers_contacts", status_code=HTTP_201_CREATED)
def add_supplier_contact(supplier_contact: SupplierContactSchema):
    db_supplier = get_supplier(supplier_contact.supplier_id)
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier_contact = Supplier_contact(name = supplier_contact.name, position = supplier_contact.position, phone = supplier_contact.phone, email = supplier_contact.email, supplier_id = supplier_contact.supplier_id)
    session = get_session()
    session.add(new_supplier_contact)
    session.commit()
    return Response(status_code=HTTP_201_CREATED)

@suppliers_contacts.get("/api/suppliers_contacts/{supplier_contact_id}", response_model=SupplierContactSchema)
def get_supplier_contact(supplier_contact_id: int):
    return get_session().query(Supplier_contact).filter(Supplier_contact.id == supplier_contact_id).first()

@suppliers_contacts.get("/api/supplier_contacts/{supplier_id}", response_model=List[SupplierContactSchema])
def get_supplier_contacts(supplier_id: int):
    return get_session().query(Supplier_contact).filter(Supplier_contact.supplier_id == supplier_id).all()

@suppliers_contacts.put("/api/suppliers_contacts/{supplier_contact_id}", response_model=SupplierContactSchema)
def update_supplier_contact(data_update: SupplierContactSchema, supplier_contact_id: int):
    db_supplier_contact = get_supplier_contact(supplier_contact_id)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_supplier_contact, key, value)
    session = get_session()
    session.add(db_supplier_contact)
    session.commit()
    session.refresh(db_supplier_contact)
    return db_supplier_contact

@suppliers_contacts.delete("/api/suppliers_contacts/{supplier_contact_id}", status_code=HTTP_204_NO_CONTENT)
def delete_supplier_contact(supplier_id: int):
    db_supplier_contact = get_supplier_contact(supplier_id)
    if not db_supplier_contact:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_supplier_contact)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)