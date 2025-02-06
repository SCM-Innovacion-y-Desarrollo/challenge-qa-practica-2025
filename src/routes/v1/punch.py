"""This module contains the enroll routes."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.models import Punch, PunchTypeEnum
from src.schemas import PunchDBModel, PunchPinModel, ResponseModel

from .devices import get_device_by_id
from .employees import get_employee_by_dni

_punch = APIRouter()

"""
    crear endpoint para obtener todos los punches con diversos filtros sobre los campos de punch,
    TODO: deberá crear casos de pruebas para que otro desarrollador lo pueda implementar siguiendo las pruebas
"""


@_punch.post("/pin", tags=["punch"], response_model=ResponseModel[PunchDBModel])
async def create_punch(
    data: PunchPinModel, db: Session = Depends(get_db)
):
    """
    Crea un nuevo punch.

    Si hay algun campo faltante igualmente debe guardar el punch.
    Si hay algun error o falta algun campo o algun elemento no se encuentra en la base de datos
    se debería agregar en campo status del Punch
    """

    employee = await get_employee_by_dni(data.dni, db)
    device = await get_device_by_id(data.dni, db)

    """ TODO: identificar posibles errores o validaciones faltantes en el flujo para indicarlo en status"""

    punch = Punch(
        device_id=device.id,
        timezone=device.timezone,
        punch_dtm=datetime.now(timezone.utc),
        punch_type=PunchTypeEnum.pin,
        dni=data.dni,
        status="",
        employee_id=employee.id,
        pin=data.pin,
    )

    db.add(punch)
    db.commit()
    return {"data": punch}
