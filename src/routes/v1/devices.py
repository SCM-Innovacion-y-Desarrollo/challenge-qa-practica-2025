from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db import get_db
from src.models import DevicePunchType, Devices
from src.repository import get_all, get_by_id
from src.schemas import (DeviceDBModel, DeviceModel, DevicesDBModel,
                         ResponseModel)

_devices = APIRouter()


@_devices.get("", tags=["devices"], response_model=ResponseModel[DevicesDBModel])
async def devices(db: Session = Depends(get_db)):
    """Get all devices."""
    devices = fetch_all_devices(db)
    return {"data": devices}

def fetch_all_devices(db):
    """ TODO: realizar casos de pruebas a la funcion fetch_all_devices ya que despues se le agregará un flujo"""
    return get_all(db, Devices)


@_devices.get(
    "/{device_id}", tags=["devices"], response_model=ResponseModel[DeviceDBModel]
)
async def device_by_id(
    device_id: Annotated[int, Path(title="The ID of the item to get")],
    db: Session = Depends(get_db),
):
    """Get a device by ID."""
    device = await get_device_by_id(device_id, db)
    return {"data": device}


async def get_device_by_id(device_id, db) -> Devices:
    """Get a device by ID."""
    return get_by_id(db, Devices, device_id)


@_devices.post("", tags=["devices"], response_model=ResponseModel[DeviceDBModel])
async def device_create(
    device: DeviceModel, db: Session = Depends(get_db)
):
    """Create a new device."""
    new_device = Devices(**device.model_dump(exclude=["pin"]))
    db.add(new_device)
    db.flush()

    new_device_punch_type = DevicePunchType(**device.model_dump(include=["pin"]))
    new_device_punch_type.device_id = new_device.id
    db.add(new_device_punch_type)
    db.commit()

    device = await get_device_by_id(new_device.id, db)
    return {"data": device}

