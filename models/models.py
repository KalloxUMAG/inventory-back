from sqlalchemy import Integer, String, LargeBinary, Date, Boolean, Sequence
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, Optional
from config.database import Base

# Tablas independientes


class Buildings(Base):
    __tablename__ = "Buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    units: Mapped[List['Units']] = relationship("Units", backref="Buildings", cascade="delete,merge")

class Invoices(Base):
    __tablename__ = "Invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Suppliers.id", ondelete="CASCADE"))
    equipments: Mapped[List['Equipments']] = relationship("Equipments", backref="Invoices")
    date = mapped_column(Date)

class Brands(Base):
    __tablename__ = "Brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    models: Mapped[List['Models']] = relationship("Models", backref="Brands", cascade="all, delete")

class Models(Base):
    __tablename__ = "Models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    model_numbers: Mapped[List['Model_numbers']] = relationship("Model_numbers", backref="Models", cascade="all, delete")
    brand_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Brands.id", ondelete="CASCADE"))

class Model_numbers(Base):
    __tablename__ = "Model_numbers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String, nullable=False)
    equipments: Mapped[List['Equipments']] = relationship("Equipments", backref="Model_numbers")
    model_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Models.id", ondelete="CASCADE"))

class Projects(Base):
    __tablename__ = "Projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("Project_owners.id", ondelete="CASCADE"))
    stages: Mapped[List['Stages']] = relationship("Stages", backref="Projects", cascade="delete,merge")
    equipments: Mapped[List['Stages']] = relationship("Equipments", secondary="Equipments_has_Projects", back_populates="projects")

class Project_owners(Base):
    __tablename__ = "Project_owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    projects: Mapped[List['Projects']] = relationship("Projects", backref="Project_owners", cascade="delete,merge")

class Suppliers(Base):
    __tablename__ = "Suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    rut: Mapped[str] = mapped_column(String)
    supplier_contacts: Mapped[List['Supplier_contact']] = relationship("Supplier_contact", backref="Suppliers", cascade="delete,merge")
    city_address = mapped_column(String)
    invoices: Mapped[List['Invoices']] = relationship("Invoices", backref="Suppliers", cascade="delete,merge")
    equipments: Mapped[List['Equipments']] = relationship("Equipments", backref="Suppliers")


# Tablas dependientes


class Equipments(Base):
    __tablename__ = "Equipments"

    id: Mapped[int] = mapped_column(Integer, Sequence('equipment_id_seq'), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    serial_number: Mapped[Optional[str]] = mapped_column(String)
    umag_inventory_code: Mapped[Optional[str]] = mapped_column(String)
    reception_date = mapped_column(Date)
    maintenance_period: Mapped[Optional[int]] = mapped_column(Integer)
    observation: Mapped[Optional[str]] = mapped_column(String)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Suppliers.id", ondelete="SET NULL"))
    invoice_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Invoices.id", ondelete="SET NULL"))
    model_number_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Model_numbers.id", ondelete="SET NULL"))
    room_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Rooms.id", ondelete="SET NULL"))
    maintenances: Mapped[List['Maintenances']] = relationship("Maintenances", backref="Equipments", cascade="delete,merge")
    projects: Mapped[List['Projects']] = relationship("Projects", secondary="Equipments_has_Projects", back_populates="equipments")
    last_preventive_mainteinance = mapped_column(Date)

class Maintenances(Base):
    __tablename__ = "Maintenances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date = mapped_column(Date)
    observations: Mapped[str] = mapped_column(String)
    equiptment_id: Mapped[int] = mapped_column(Integer, ForeignKey("Equipments.id", ondelete="CASCADE"))
    maintenance_type: Mapped[str] = mapped_column(String)

class Rooms(Base):
    __tablename__ = "Rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    unit_id: Mapped[int] = mapped_column(Integer, ForeignKey("Units.id", ondelete="CASCADE"))
    equipments: Mapped[List['Equipments']] = relationship("Equipments", backref="Rooms")


class Stages(Base):
    __tablename__ = "Stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"))
    equipments_has_projects: Mapped[int] = relationship("Equipments_has_Projects", backref="Stages")

class Supplier_contact(Base):
    __tablename__ = "Supplier_contact"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("Suppliers.id", ondelete="CASCADE"))


class Units(Base):
    __tablename__ = "Units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("Buildings.id", ondelete="CASCADE"))
    rooms: Mapped[List['Rooms']] = relationship("Rooms", backref="Units", cascade="delete,merge")

# Relaciones N - M

class Equipments_has_Projects(Base):
    __tablename__ = "Equipments_has_Projects"

    equipment_id = mapped_column(Integer, ForeignKey("Equipments.id", ondelete="CASCADE"), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"), primary_key=True)
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey("Stages.id"))
