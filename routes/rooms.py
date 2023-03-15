from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from config.database import get_session
from models.models import Rooms
from schemas.room_schema import RoomSchema
from typing import List

from routes.units import get_unit

rooms = APIRouter()

@rooms.get("/api/rooms", response_model=List[RoomSchema])
def get_rooms():
    result = get_session().query(Rooms).all()
    return result

@rooms.post("/api/rooms", status_code=HTTP_201_CREATED)
def add_room(room: RoomSchema):
    db_unit = get_unit(room.unit_id)
    if not db_unit:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_room = Rooms(name = room.name, unit_id = room.unit_id)
    session = get_session()
    session.add(new_room)
    session.commit()
    content = str(new_room.id)
    return Response(status_code=HTTP_201_CREATED, content=content)

@rooms.get("/api/room/{room_id}", response_model=RoomSchema)
def get_room(room_id: int):
    return get_session().query(Rooms).filter(Rooms.id == room_id).first()

@rooms.get("/api/rooms/{unit_id}", response_model=List[RoomSchema])
def get_rooms_unit(unit_id: int):
    return get_session().query(Rooms).filter(Rooms.unit_id == unit_id).all()

@rooms.put("/api/rooms/{room_id}", response_model=RoomSchema)
def update_room(data_update: RoomSchema, room_id: int):
    db_room = get_room(room_id)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    session = get_session()
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room

@rooms.delete("/api/rooms/{room_id}", status_code=HTTP_204_NO_CONTENT)
def delete_room(room_id: int):
    db_room = get_room(room_id)
    if not db_room:
        return Response(status_code=HTTP_404_NOT_FOUND)
    session = get_session()
    session.delete(db_room)
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)