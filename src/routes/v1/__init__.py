from fastapi import APIRouter

from src.routes.v1.devices import _devices
from src.routes.v1.employees import _employees
from src.routes.v1.enroll import _enroll
from src.routes.v1.punch import _punch

_v1 = APIRouter()

_v1.include_router(_devices, prefix="/devices")
_v1.include_router(_employees, prefix="/employees")
_v1.include_router(_enroll, prefix="/enroll")
_v1.include_router(_punch, prefix="/punch")
