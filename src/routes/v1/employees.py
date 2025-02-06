from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.db import get_db
from src.models import Employee
from src.repository import get_all, get_by_id
from src.schemas import EmployeeDataModel, EmployeeDBModel, ResponseModel

_employees = APIRouter()


@_employees.get("", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employees(db: Session = Depends(get_db)):
    """Get all employees."""
    """TODO: Deberá realizar casos de prueba para los parametros de filtro de empleados"""
    empleados = filtrar_empleados(db)
    return {"data": empleados}


def filtrar_empleados(db: Session, **kargs) -> list[Employee]:
    """
        Filtrado de empleados.
        según los campos del Employee

    """
    return get_all(db, Employee)


@_employees.get(
    "/{employee_id}", tags=["employees"]
)
async def employee_by_id(
    employee_id: Annotated[int, Path(title="The ID of the item to get")],
    db: Session = Depends(get_db),
):
    """Get an employee by ID."""
    employee = await get_employee_by_id(employee_id, db)
    return {"data": "employee"}


async def get_employee_by_id(employee_id, db: Session) -> Employee:
    """Get an employee by ID."""
    return get_by_id(db, Employee, employee_id)


async def get_employee_by_dni(dni, db: Session) -> Employee:
    """Get an employee by DNI."""
    return db.query(Employee).filter(Employee.dni == dni).first()


@_employees.post("", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_create(
    employee: EmployeeDataModel, db: Session = Depends(get_db)
):
    """Create a new employee."""

    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    return {"data": new_employee}


@_employees.delete(
    "/{employee_id}", tags=["employees"], response_model=ResponseModel[EmployeeDBModel]
)
async def employee_delete(
    employee_id: Annotated[int, Path(title="The ID of the item to get")],
    db: Session = Depends(get_db),
):
    """Delete an employee."""
    employee: Employee = get_by_id(db, Employee, employee_id)
    d_data = EmployeeDBModel.model_validate(employee)
    db.delete(employee)
    db.commit()
    return {"data": d_data}
