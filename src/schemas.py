from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from src.models import PunchTypeEnum

M = TypeVar("M", bound=BaseModel)
T = TypeVar("T", bound=BaseModel)


class ResponseModel(BaseModel, Generic[M]):
    status: Optional[str] = "success"
    data: List[M] | M


class InputModel(BaseModel, Generic[T]):
    data: T


class LoginModel(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
    type: str | None = None


class PinModel(BaseModel):
    pin: int


class PunchTypeValuesModel(BaseModel):
    pin: Optional[str]


class PunchTypeModel(BaseModel):
    pin: bool


class DevicesDBModel(BaseModel):
    id: int
    name: str
    location: str
    timezone: str
    punch_type: PunchTypeModel


class DeviceModel(BaseModel):
    name: int
    location: int
    timezone: int
    pin: bool


class DeviceDBModel(BaseModel):
    id: int
    name: str
    location: str
    timezone: str
    pin: bool

    model_config = ConfigDict(from_attributes=True)


class PunchModel(BaseModel):
    device_id: int


class PunchPinModel(PunchModel):
    dni: str
    pin: int


class EmployeeDataModel(BaseModel):
    dni: str
    fullname: str
    email: str


class TokenModel(BaseModel):
    token: str


class EmployeeDBModel(EmployeeDataModel, BaseModel):
    id: int
    enrollments: Optional[PunchTypeValuesModel]

    model_config = ConfigDict(from_attributes=True)


class DniModel(BaseModel):
    dni: str


class PunchDBModel(BaseModel):
    id: int
    device_id: Optional[int]
    timezone: str
    punch_dtm: datetime
    punch_type: PunchTypeEnum
    dni: str
    status: str
    employee_id: Optional[int]
    pin: Optional[str]
