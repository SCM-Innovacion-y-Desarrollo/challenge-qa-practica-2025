"""This module contains the enroll routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db import get_db
from src.schemas import PinModel, ResponseModel

from .employees import get_employee_by_id

_enroll = APIRouter()


@_enroll.post("/{employee_id}/pin", tags=["enroll"], response_model=ResponseModel[PinModel])
async def create_pin(
    data: PinModel,
    employee_id: Annotated[int, Path(title="The ID of the item to get")],
    db: Session = Depends(get_db),
):
    """Create a new pin for an employee."""
    """ TODO: identificar posibles errores en el flujo """
    employee = await get_employee_by_id(employee_id, db)

    if not employee.enrolls:
        enroll = Enrollments(employee_id=employee.id, pin=data.pin)
    else:
        enroll = employee.enrols
        enroll.pin = data.pin

    db.add(enroll)
    db.commit()
    return {"data": enroll}
